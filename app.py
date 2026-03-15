from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for
from services.storage import (
    create_source,
    get_all_sources,
    get_source,
    save_source,
    add_history_entry,
    delete_source,
)
from services.extractor import extract_source_content
from services.summarizer import summarize_text
from services.update_checker import get_update_status

app = Flask(__name__)


@app.route("/")
def dashboard():
    sources = get_all_sources()
    message = request.args.get("message", "")
    return render_template("dashboard.html", sources=sources, message=message)


@app.route("/add", methods=["POST"])
def add_source():
    url = request.form.get("url", "").strip()

    if not url:
        return redirect(url_for("dashboard", message="Please enter a valid URL"))

    extracted_title = "Untitled Source"
    try:
        content = extract_source_content(url)
        if content.get("title"):
            extracted_title = content["title"]
    except Exception:
        # If extraction fails here, still create the source with fallback title
        pass

    result = create_source(url, title=extracted_title)

    if result["created"]:
        return redirect(url_for("source_page", source_id=result["source_id"]))

    return redirect(url_for("source_page", source_id=result["source_id"], message=result["message"]))


@app.route("/summarise/<source_id>", methods=["POST"])
def summarise_source(source_id):
    source = get_source(source_id)
    if not source:
        return "Source not found", 404

    try:
        content = extract_source_content(source["url"])
        text = content["text"]
        extracted_title = content.get("title", "").strip()

        if extracted_title:
            source["title"] = extracted_title

        result = summarize_text(text, title=source.get("title", "Untitled Source"))

        source["text"] = text
        source["summary"] = result["summary"]
        source["medium_draft"] = result["medium_draft"]
        source["excerpts"] = result["excerpts"]
        source["status"] = "Summarised"

        if not source.get("created_at"):
            source["created_at"] = add_history_entry(source, "Initial Summary Created")["history"][-1]["date"]
        else:
            source = add_history_entry(source, "Summary Regenerated")

        save_source(source)

    except Exception as e:
        return f"Error during summarisation: {str(e)}", 500

    return redirect(url_for("source_page", source_id=source_id))


@app.route("/check-updates/<source_id>", methods=["POST"])
def check_updates(source_id):
    source = get_source(source_id)
    if not source:
        return "Source not found", 404

    try:
        old_text = source.get("text", "")
        content = extract_source_content(source["url"])
        new_text = content["text"]
        new_title = content.get("title", "").strip()

        if new_title:
            source["title"] = new_title

        status = get_update_status(old_text, new_text)

        if status == "Update detected":
            result = summarize_text(new_text, title=source.get("title", "Untitled Source"))

            source["pending_update"] = {
                "old_summary": source.get("summary", []),
                "new_summary": result["summary"],
                "checked_at": add_history_entry(source, "Update detected")["history"][-1]["date"],
            }
            source["status"] = "Update detected"
        else:
            source["status"] = "No change detected"
            source["last_checked"] = add_history_entry(source, "No change detected")["history"][-1]["date"]
            source.pop("pending_update", None)

        save_source(source)

    except Exception as e:
        return f"Error during update check: {str(e)}", 500

    return redirect(url_for("source_page", source_id=source_id))


@app.route("/accept-update/<source_id>", methods=["POST"])
def accept_update(source_id):
    source = get_source(source_id)
    if not source:
        return "Source not found", 404

    pending = source.get("pending_update")
    if pending:
        source["summary"] = pending.get("new_summary", source.get("summary", []))
        source["status"] = "Summarised"
        source["last_checked"] = pending.get("checked_at", source.get("last_checked", ""))
        source = add_history_entry(source, "Update accepted")
        source.pop("pending_update", None)
        save_source(source)

    return redirect(url_for("source_page", source_id=source_id))


@app.route("/delete/<source_id>", methods=["POST"])
def delete_source_route(source_id):
    delete_source(source_id)
    return redirect(url_for("dashboard"))


@app.route("/source/<source_id>")
def source_page(source_id):
    source = get_source(source_id)
    if not source:
        return "Source not found", 404

    message = request.args.get("message", "")
    return render_template("source.html", source=source, message=message)


@app.route("/history/<source_id>")
def history_page(source_id):
    source = get_source(source_id)
    if not source:
        return "Source not found", 404
    return render_template("history.html", source=source)


if __name__ == "__main__":
    app.run(debug=True)