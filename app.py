from flask import Flask, request,Response
from hijri_calendar_consistent import calculate_hijri_calendar

app = Flask(__name__)
hijri_calendar = calculate_hijri_calendar()

@app.route('/', methods=['GET'])
def mainroute():
     return 'Please enter / followed by the Gregorian year you need to get the corresponding Hijri year in the URL OR enter /hijri_calendar in the URL to get Text File contains all Hijri Calnder '

@app.route('/hijri_calendar')
def generate_hijri_calendar():
    # Start with a header
    output_str = "Hijri Calendar\n\n"

    # Iterate over the years
    for year, months in hijri_calendar.items():
        output_str += f"Year: {year}\n"  # Add the year header
        output_str += "-" * 50 + "\n"  # Add a separator line

        # Iterate over the months in the year
        for month_data in months:
            # Access values using keys instead of indices
            output_str += f"{month_data['month_name']} {month_data['days_in_month']}\t\t\t\t\t\t\t\t\t\t\t\t\t\t{month_data['eclipse']}\n"
            output_str += f"\tFull Moon Observed: {month_data['full_moon_start']} - {month_data['full_moon_end']}\n"
            output_str += f"\tHijri (Gregorian): {month_data['hijri_start']} - {month_data['hijri_end']}\n"
            output_str += f"\tHijri (Natural): {month_data['hijri_natural_start']} - {month_data['hijri_natural_end']}\n"
            output_str += "\n"  # Empty line for separation

        output_str += "\n"  # Add an empty line between years

    # Serve the content as a downloadable text file
    return Response(
        output_str,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=hijri_calendar.txt"}
    )

@app.route('/<int:year>', methods=['GET', 'POST'])
def get_hijri_calendar(year):
    if year < 622 or year > 3999 :
        return 'The Hijri calendar starts in the year 622 of the Gregorian calendar. Please enter a valid Gregorian year (must be greater than 621). /n Our calendar is valid until the year 3999 in the Gregorian calendar. '

    # Prepare the output in the desired format
    output_str = ""
    
    # Iterate over years in the output dictionary
    for month_data in hijri_calendar[year-621]:
        # Build the formatted output string for each month
        output_str += f"{month_data['month_name']} {month_data['days_in_month']}\t\t\t\t\t\t\t\t\t\t\t\t\t\t{month_data['eclipse']}\n"
        output_str += f"\tFull Moon Observed: {month_data['full_moon_start']} - {month_data['full_moon_end']}\n"
        output_str += f"\tHijri (Gregorian): {month_data['hijri_start']} - {month_data['hijri_end']}\n"
        output_str += f"\tHijri (Natural): {month_data['hijri_natural_start']} - {month_data['hijri_natural_end']}\n"
        output_str += "\n"  # Empty line for separation
    
    # Return the response as plain text
    return Response(output_str, mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)