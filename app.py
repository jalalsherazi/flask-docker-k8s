from flask import Flask, render_template

app = Flask(__name__)

people = [
    {"id": 1, "name": "jalal"},
    {"id": 2, "name": "saqlain"},
    {"id": 3, "name": "haroon"},
    {"id": 4, "name": "ubaid"}
]


@app.route("/")
def people_list():
    return render_template("people.html", people=people)


@app.route("/person/<int:person_id>")
def person_detail(person_id):
    person = next((p for p in people if p["id"] == person_id), None)

    if person is None:
        return "Person not found", 404

    return render_template("person.html", person=person)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
