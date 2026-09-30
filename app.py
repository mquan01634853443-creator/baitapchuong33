from flask import Flask, render_template, jsonify, request, abort
import json

app = Flask(__name__)


# Đọc danh sách sách từ books.json
def load_books():
    with open("books.json", "r", encoding="utf-8") as file:
        return json.load(file)


# =========================
# TRANG CHỦ
# =========================
@app.route("/")
def home():
    books = load_books()

    total_books = len(books)
    available_books = sum(
        1 for book in books
        if book["available"]
    )

    return render_template(
        "index.html",
        total_books=total_books,
        available_books=available_books
    )


# =========================
# DANH SÁCH SÁCH
# /books
# /books?category=Web
# =========================
@app.route("/books")
def books():
    books = load_books()

    category = request.args.get("category")

    if category:
        books = [
            book
            for book in books
            if book["category"].lower() == category.lower()
        ]

    return render_template(
        "books.html",
        books=books,
        category=category
    )


# =========================
# CHI TIẾT SÁCH
# /books/1
# =========================
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    books = load_books()

    book = next(
        (
            book
            for book in books
            if book["id"] == book_id
        ),
        None
    )

    if book is None:
        abort(404)

    return render_template(
        "detail.html",
        book=book
    )


# =========================
# API CHI TIẾT SÁCH
# /api/books/1
# =========================
@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    books = load_books()

    book = next(
        (
            book
            for book in books
            if book["id"] == book_id
        ),
        None
    )

    if book is None:
        return jsonify({
            "error": f"Không có sách với ID = {book_id}"
        }), 404

    return jsonify(book)


# =========================
# TRANG 404
# =========================
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# =========================
# CHẠY FLASK
# =========================
if __name__ == "__main__":
    app.run(debug=True)