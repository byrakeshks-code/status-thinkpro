from flask import Flask, render_template_string

app = Flask(__name__)

# ============================================
# BACKEND DATA
# Edit only these values
# ============================================
BOOK_DATA = {
    "Grade 1": {
        "total_comics": 37,
        "total_activities": 37,
        "total_infographics": 15,
        "completed_comics": 32,
        "completed_activities": 37,
        "completed_infographics": 15,
    },
    "Grade 2": {
        "total_comics": 37,
        "total_activities": 37,
        "total_infographics": 18,
        "completed_comics": 20,
        "completed_activities": 15,
        "completed_infographics": 5,
    }
}

# ============================================
# TIMELINE DATA
# Edit only these values
# ============================================
TIMELINE_EVENTS = [
    {
        "title": "Project Started",
        "date": "2026-04-13",
        "description": "Initial planning and structure setup for both grades.",
        "status": "Completed"
    },
    {
        "title": "Comic Ideation",
        "date": "2026-04-14",
        "description": "Comic writing and illustration work in progress.",
        "status": "Completed"
    },
    {
        "title": "Comic Generation",
        "date": "2026-04-15",
        "description": "Started Production for Comics",
        "status": "Active"
    },
    {
        "title": "Infographic and Activities Production",
        "date": "2026-04-18",
        "description": "Ideated Activities and Infographics and Deployed Resources",
        "status": "Active"
    },
    {
        "title": "Daily Progress Update-1",
        "date": "2026-04-21",
        "description": "G1: 54%, G2: 15% ",
        "status": "Completed"
    },
    {
        "title": "Daily Progress Update-2",
        "date": "2026-04-22",
        "description": "G1: 57.3% , G2: 16.67%",
        "status": "Completed"
    },
    {
        "title": "Daily Progress Update-3",
        "date": "2026-04-23",
        "description": "G1: 66.2%, G2: 30.23%",
        "status": "Completed"
    },
    {
        "title": "Daily Progress Update-4",
        "date": "2026-04-24",
        "description": "G1: 75.28%, G2: 39.13%",
        "status": "Completed"
    },
    {
        "title": "Daily Progress Update-4",
        "date": "2026-04-25",
        "description": "G1: 87.64%, G2: 43.48%",
        "status": "Completed"
    },
    {
        "title": "Daily Progress Update-5",
        "date": "2026-04-26",
        "description": "Sunday, Scripts Improvised",
        "status": "Completed"
    },
    {
        "title": "Daily Progress Update-6",
        "date": "2026-04-27",
        "description": "G1: 94.38%, G2: 43.48%",
        "status": "Completed"
    },
    {
        "title": "Daily Progress Update-6",
        "date": "2026-04-28",
        "description": "Update will be posted",
        "status": "Pending"
    },
    {
        "title": "Final Review",
        "date": "2026-04-30",
        "description": "QA pass, corrections, and final completion check.",
        "status": "Pending"
    }
]


# ============================================
# LOGIC
# ============================================
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def percent(done, total):
    done = clamp(done, 0, total)
    return round((done / total) * 100, 2) if total > 0 else 0


def overall_book_numbers(completed_comics, total_comics, completed_activities, total_activities, completed_infographics, total_infographics):
    done_items = (
        clamp(completed_comics, 0, total_comics) +
        clamp(completed_activities, 0, total_activities) +
        clamp(completed_infographics, 0, total_infographics)
    )
    total_items = total_comics + total_activities + total_infographics
    return done_items, total_items


def build_progress():
    result = {}

    for grade, data in BOOK_DATA.items():
        total_comics = data.get("total_comics", 0)
        total_activities = data.get("total_activities", 0)
        total_infographics = data.get("total_infographics", 0)

        comics_done = data.get("completed_comics", 0)
        activities_done = data.get("completed_activities", 0)
        infographics_done = data.get("completed_infographics", 0)

        overall_done, overall_total = overall_book_numbers(
            comics_done,
            total_comics,
            activities_done,
            total_activities,
            infographics_done,
            total_infographics,
        )

        result[grade] = {
            "comics_done": clamp(comics_done, 0, total_comics),
            "activities_done": clamp(activities_done, 0, total_activities),
            "infographics_done": clamp(infographics_done, 0, total_infographics),
            "overall_done": overall_done,

            "comics_total": total_comics,
            "activities_total": total_activities,
            "infographics_total": total_infographics,
            "overall_total": overall_total,

            "comics_percent": percent(comics_done, total_comics),
            "activities_percent": percent(activities_done, total_activities),
            "infographics_percent": percent(infographics_done, total_infographics),
            "overall_percent": percent(overall_done, overall_total),
        }

    return result


# ============================================
# FRONTEND
# 4 bars per grade + timeline section
# ============================================
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Progress Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 30px;
            color: #222;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        h1 {
            margin-bottom: 24px;
            font-size: 52px;
            font-weight: 800;
        }

        .card {
            background: #fff;
            border-radius: 18px;
            padding: 28px;
            margin-bottom: 28px;
            box-shadow: 0 6px 22px rgba(0, 0, 0, 0.08);
        }

        .section-title {
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 22px;
        }

        .grade-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 18px;
        }

        .grade-title {
            font-size: 28px;
            font-weight: 800;
        }

        .overall-text {
            font-size: 18px;
            font-weight: 700;
            color: #0d6efd;
        }

        .progress-block {
            margin-bottom: 22px;
        }

        .progress-block.small {
            margin-bottom: 20px;
        }

        .label-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: 700;
        }

        .bar {
            width: 100%;
            height: 22px;
            background: #e6eaf0;
            border-radius: 999px;
            overflow: hidden;
        }

        .bar.large {
            height: 40px;
        }

        .fill {
            height: 100%;
            border-radius: 999px;
            transition: width 0.4s ease;
        }

        .overall-fill {
            background: linear-gradient(90deg, #2563eb, #3b82f6);
        }

        .comics {
            background: #3b82f6;
        }

        .activities {
            background: #10b981;
        }

        .infographics {
            background: #f59e0b;
        }

        .divider {
            height: 1px;
            background: #e5e7eb;
            margin: 18px 0 24px 0;
        }

        .timeline-wrapper {
            position: relative;
            margin-top: 12px;
            padding-left: 22px;
        }

        .timeline-line {
            position: absolute;
            left: 7px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: #dbe3ee;
            border-radius: 999px;
        }

        .timeline-item {
            position: relative;
            margin-bottom: 24px;
            padding-left: 22px;
        }

        .timeline-item:last-child {
            margin-bottom: 0;
        }

        .timeline-dot {
            position: absolute;
            left: -1px;
            top: 6px;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            border: 3px solid #fff;
            box-shadow: 0 0 0 2px #dbe3ee;
            background: #cbd5e1;
        }

        .timeline-dot.Completed {
            background: #10b981;
            box-shadow: 0 0 0 2px #10b98133;
        }

        .timeline-dot.Active {
            background: #3b82f6;
            box-shadow: 0 0 0 2px #3b82f633;
        }

        .timeline-dot.Pending {
            background: #f59e0b;
            box-shadow: 0 0 0 2px #f59e0b33;
        }

        .timeline-content {
            background: #f9fbfd;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 16px 18px;
        }

        .timeline-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }

        .timeline-title {
            font-size: 18px;
            font-weight: 800;
        }

        .timeline-date {
            font-size: 14px;
            font-weight: 700;
            color: #64748b;
        }

        .timeline-desc {
            font-size: 15px;
            line-height: 1.5;
            color: #334155;
        }

        .timeline-status {
            display: inline-block;
            margin-top: 10px;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }

        .status-done {
            background: #dcfce7;
            color: #166534;
        }

        .status-active {
            background: #dbeafe;
            color: #1d4ed8;
        }

        .status-pending {
            background: #fef3c7;
            color: #92400e;
        }

        .footnote {
            margin-top: 10px;
            color: #666;
            font-size: 14px;
        }

        @media (max-width: 640px) {
            body {
                padding: 16px;
            }

            h1 {
                font-size: 36px;
            }

            .grade-title,
            .section-title {
                font-size: 22px;
            }

            .label-row {
                font-size: 14px;
            }

            .bar.large {
                height: 30px;
            }

            .timeline-title {
                font-size: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Project Progress Dashboard</h1>

        {% for grade, item in progress.items() %}
        <div class="card">
            <div class="grade-header">
                <div class="grade-title">{{ grade }}</div>
                <div class="overall-text">Overall Book Completion: {{ item.overall_percent }}%</div>
            </div>

            <div class="progress-block">
                <div class="label-row">
                    <span>Overall Completion</span>
                    <span>{{ item.overall_done }} / {{ item.overall_total }} ({{ item.overall_percent }}%)</span>
                </div>
                <div class="bar large">
                    <div class="fill overall-fill" style="width: {{ item.overall_percent }}%;"></div>
                </div>
            </div>

            <div class="divider"></div>

            <div class="progress-block small">
                <div class="label-row">
                    <span>Comics</span>
                    <span>{{ item.comics_done }} / {{ item.comics_total }} ({{ item.comics_percent }}%)</span>
                </div>
                <div class="bar">
                    <div class="fill comics" style="width: {{ item.comics_percent }}%;"></div>
                </div>
            </div>

            <div class="progress-block small">
                <div class="label-row">
                    <span>Activities</span>
                    <span>{{ item.activities_done }} / {{ item.activities_total }} ({{ item.activities_percent }}%)</span>
                </div>
                <div class="bar">
                    <div class="fill activities" style="width: {{ item.activities_percent }}%;"></div>
                </div>
            </div>

            <div class="progress-block small">
                <div class="label-row">
                    <span>Infographics</span>
                    <span>{{ item.infographics_done }} / {{ item.infographics_total }} ({{ item.infographics_percent }}%)</span>
                </div>
                <div class="bar">
                    <div class="fill infographics" style="width: {{ item.infographics_percent }}%;"></div>
                </div>
            </div>
        </div>
        {% endfor %}

        <div class="card">
            <div class="section-title">Project Timeline</div>

            <div class="timeline-wrapper">
                <div class="timeline-line"></div>

                {% for event in timeline %}
                <div class="timeline-item">
                    <div class="timeline-dot {{ event.status }}"></div>

                    <div class="timeline-content">
                        <div class="timeline-top">
                            <div class="timeline-title">{{ event.title }}</div>
                            <div class="timeline-date">{{ event.date }}</div>
                        </div>

                        <div class="timeline-desc">{{ event.description }}</div>

                        <div class="timeline-status status-{{ event.status }}">
                            {{ event.status }}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="footnote">
            Last Updated: 24 Apr 2026, 05:44 PM.
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def dashboard():
    progress = build_progress()
    return render_template_string(HTML, progress=progress, timeline=TIMELINE_EVENTS)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
