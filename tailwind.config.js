/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./contacts/templates/**/*.html", "./contacts/static/js/**/*.js"],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
};
