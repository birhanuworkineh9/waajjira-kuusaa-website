from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("karooraa.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                sector TEXT NOT NULL,
                plan_year TEXT NOT NULL,
                quarter TEXT NOT NULL,
                objective TEXT,
                activity TEXT NOT NULL,
                responsible TEXT,
                start_date TEXT,
                due_date TEXT,
                budget REAL NOT NULL DEFAULT 0,
                spent REAL NOT NULL DEFAULT 0,
                progress INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'Karoorfame',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()


@app.route("/")
def index():
    with get_db() as db:
        plans = db.execute("SELECT * FROM plans ORDER BY id DESC").fetchall()
        stats = db.execute("""
            SELECT COUNT(*) AS total,
                   COALESCE(SUM(budget), 0) AS budget,
                   COALESCE(SUM(spent), 0) AS spent,
                   COALESCE(AVG(progress), 0) AS progress
            FROM plans
        """).fetchone()
    return render_template("index.html", plans=plans, stats=stats)


@app.route("/add", methods=["GET", "POST"])
def add_plan():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        activity = request.form.get("activity", "").strip()
        if not title or not activity:
            flash("Mata-duree fi hojii karoorfame guuti.", "error")
            return redirect(url_for("add_plan"))

        def money(name):
            try:
                return max(0, float(request.form.get(name, "0") or 0))
            except ValueError:
                return 0

        try:
            progress = int(request.form.get("progress", "0") or 0)
        except ValueError:
            progress = 0
        progress = min(100, max(0, progress))
        status = request.form.get("status", "Karoorfame")
        allowed_statuses = ["Karoorfame", "Hojjetamaa jira", "Xumurame", "Harkifate"]
        if status not in allowed_statuses:
            status = "Karoorfame"

        with get_db() as db:
            db.execute("""
                INSERT INTO plans
                (title, sector, plan_year, quarter, objective, activity, responsible,
                 start_date, due_date, budget, spent, progress, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                title,
                request.form.get("sector", "Waliigala"),
                request.form.get("plan_year", "").strip() or "2019",
                request.form.get("quarter", "Kurmaana 1"),
                request.form.get("objective", "").strip(),
                activity,
                request.form.get("responsible", "").strip(),
                request.form.get("start_date") or None,
                request.form.get("due_date") or None,
                money("budget"),
                money("spent"),
                progress,
                status,
                request.form.get("notes", "").strip()
            ))
            db.commit()
        flash("Karoora haala gaariin kuufameera.", "success")
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/edit/<int:plan_id>", methods=["GET", "POST"])
def edit_plan(plan_id):
    with get_db() as db:
        plan = db.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
        if plan is None:
            flash("Karoora kana hin argamne.", "error")
            return redirect(url_for("index"))
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            activity = request.form.get("activity", "").strip()
            if not title or not activity:
                flash("Mata-duree fi hojii karoorfame guuti.", "error")
                return redirect(url_for("edit_plan", plan_id=plan_id))

            def money(name):
                try:
                    return max(0, float(request.form.get(name, "0") or 0))
                except ValueError:
                    return 0

            try:
                progress = min(100, max(0, int(request.form.get("progress", "0") or 0)))
            except ValueError:
                progress = 0
            status = request.form.get("status", "Karoorfame")
            if status not in ["Karoorfame", "Hojjetamaa jira", "Xumurame", "Harkifate"]:
                status = "Karoorfame"
            db.execute("""
                UPDATE plans SET title=?, sector=?, plan_year=?, quarter=?, objective=?,
                activity=?, responsible=?, start_date=?, due_date=?, budget=?, spent=?,
                progress=?, status=?, notes=? WHERE id=?
            """, (
                title, request.form.get("sector", "Waliigala"),
                request.form.get("plan_year", "").strip() or "2019",
                request.form.get("quarter", "Kurmaana 1"),
                request.form.get("objective", "").strip(), activity,
                request.form.get("responsible", "").strip(),
                request.form.get("start_date") or None, request.form.get("due_date") or None,
                money("budget"), money("spent"), progress, status,
                request.form.get("notes", "").strip(), plan_id
            ))
            db.commit()
            flash("Karoora haaromfameera.", "success")
            return redirect(url_for("index"))
    return render_template("add.html", plan=plan, editing=True)


@app.route("/delete/<int:plan_id>", methods=["POST"])
def delete_plan(plan_id):
    with get_db() as db:
        db.execute("DELETE FROM plans WHERE id = ?", (plan_id,))
        db.commit()
    flash("Karoora haqameera.", "success")
    return redirect(url_for("index"))


@app.route("/report")
def report():
    with get_db() as db:
        rows = db.execute("""
            SELECT sector, COUNT(*) AS count, COALESCE(SUM(budget),0) AS budget,
                   COALESCE(SUM(spent),0) AS spent, COALESCE(AVG(progress),0) AS progress
            FROM plans GROUP BY sector ORDER BY sector
        """).fetchall()
    return render_template("report.html", rows=rows)


init_db()

if __name__ == "__main__":
    app.run(debug=True)
