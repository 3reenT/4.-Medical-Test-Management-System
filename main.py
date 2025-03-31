
from datetime import datetime
import re
from datetime import datetime, timedelta
from datetime import datetime, timedelta

class TestRecord:
    def __init__(self, patient_id, test_name, test_datetime, result_value, unit, status, results_datetime=None):
        self.patient_id = patient_id
        self.test_name = test_name
        self.test_datetime = datetime.strptime(test_datetime, "%Y-%m-%d %H:%M")
        self.result_value = result_value
        self.unit = unit
        self.status = status
        if results_datetime:
            self.results_datetime = datetime.strptime(results_datetime, "%Y-%m-%d %H:%M")
        else:
            self.results_datetime = None

    def __str__(self):
        return f"{self.patient_id}: {self.test_name}, {self.test_datetime.strftime('%Y-%m-%d %H:%M')}, {self.result_value}, {self.unit}, {self.status}, {self.results_datetime.strftime('%Y-%m-%d %H:%M') if self.results_datetime else 'N/A'}"



class MedicalTest:
    def __init__(self, name, lower_bound, upper_bound, unit, turnaround_time):
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.unit = unit
        self.turnaround_time = turnaround_time

    def is_within_normal_range(self, result_value):
        return self.lower_bound <= result_value <= self.upper_bound



class Patient:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.records = []

    def add_test_record(self, test_record):
        self.records.append(test_record)

    def update_test_record(self, test_name, new_record):
        for idx, record in enumerate(self.records):
            if record.test_name == test_name:
                self.records[idx] = new_record
                break

    def get_records(self):
        return self.records

    def __str__(self):
        return f"Patient ID: {self.patient_id}, Number of Records: {len(self.records)}"


# Dictionary to store all patients
patients = {}


def add_new_medical_test():
    try:
        # Input Test Name
        name = input("Enter test name: ").strip()
        if not name:
            raise ValueError("Test name cannot be empty.")
        if name.isdigit():
            raise ValueError("Test name cannot be a number.")
        if not re.match("^[A-Za-z ]+$", name):
            raise ValueError("Test name must contain only alphabetic characters and spaces.")

        # Input Lower Bound
        lower_bound = input("Enter lower bound for normal range: ").strip()
        if not re.match(r'^-?\d+(\.\d+)?$', lower_bound):
            raise ValueError("Lower bound must be a valid number.")
        lower_bound = float(lower_bound)

        # Input Upper Bound
        upper_bound = input("Enter upper bound for normal range: ").strip()
        if not re.match(r'^-?\d+(\.\d+)?$', upper_bound):
            raise ValueError("Upper bound must be a valid number.")
        upper_bound = float(upper_bound)

        if lower_bound >= upper_bound:
            raise ValueError("Lower bound must be less than upper bound.")

        # Input Unit
        unit = input("Enter unit of the test: ").strip()
        if not unit:
            raise ValueError("Unit cannot be empty.")
        if unit.isdigit():
            raise ValueError("Test unit cannot be a number.")
        if not re.match("^[A-Za-z ]+$", unit):
            raise ValueError("Test unit must contain only alphabetic characters and spaces.")

        # Input Turnaround Time
        turnaround_time = input("Enter turnaround time (DD-hh-mm): ").strip()
        if not re.match(r'^\d{2}-\d{2}-\d{2}$', turnaround_time):
            raise ValueError("Turnaround time must be in the format DD-hh-mm.")

        # Extract days, hours, and minutes from the turnaround time
        days, hours, minutes = map(int, turnaround_time.split('-'))

        if hours >= 24:
            raise ValueError("Hours must be less than 24.")
        if minutes >= 60:
            raise ValueError("Minutes must be less than 60.")

        # Save the valid test to the file
        with open("medicalTest.txt", "a") as fo:
            fo.write(f"{name}, {lower_bound}, {upper_bound}, {unit}, {turnaround_time}\n")

        print(f"Test '{name}' added successfully.")

    except ValueError as ve:
        print(f"Error: {ve}")
    except IOError:
        print("Error: Unable to write to the file. Please check file permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def add_new_medical_test_record():
    try:
        # Input Patient ID
        patient_id = input("Enter patient ID (7 digits): ").strip()
        if not patient_id:
            raise ValueError("Patient ID cannot be empty.")
        if not re.match(r"^\d{7}$", patient_id):
            raise ValueError("Patient ID must be exactly 7 digits long and contain only numbers.")

        # Input Test Name
        test_name = input("Enter test name: ").strip()
        if not test_name:
            raise ValueError("Test name cannot be empty.")
        if test_name.isdigit():
            raise ValueError("Test name cannot be a number.")
        if not re.match("^[A-Za-z ]+$", test_name):
            raise ValueError("Test name must contain only alphabetic characters and spaces.")

        # Input Test Date and Time
        test_date_time = input("Enter test date and time (YYYY-MM-DD hh:mm): ").strip()
        try:
            test_date_time_obj = datetime.strptime(test_date_time, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Test date and time must be in the format YYYY-MM-DD hh:mm.")

        # Input Test Result
        test_result = input("Enter test result: ").strip()
        if not test_result:
            raise ValueError("Test result cannot be empty.")
        if not re.match(r'^-?\d+(\.\d+)?$', test_result):
            raise ValueError("Test result must be a valid number.")
        test_result = float(test_result)

        # Input Unit of Measurement
        unit = input("Enter unit of measurement (e.g., mg/dL): ").strip()
        if not unit:
            raise ValueError("Unit of measurement cannot be empty.")
        if not re.match("^[A-Za-z/]+$", unit):
            raise ValueError("Unit of measurement must contain only alphabetic characters and '/'.")

        # Input Status
        status = input("Enter test status (Pending, Completed, Reviewed): ").strip().capitalize()
        if status.isdigit():
            raise ValueError("Status cannot be a number.")
        if status not in ["Pending", "Completed", "Reviewed"]:
            raise ValueError("Status must be 'Pending', 'Completed', or 'Reviewed'.")

        # Input Results Date and Time if status is 'Completed'
        results_date_time = ""
        if status == "Completed":
            results_date_time = input("Enter results date and time (YYYY-MM-DD hh:mm): ").strip()
            try:
                results_date_time_obj = datetime.strptime(results_date_time, "%Y-%m-%d %H:%M")
                if results_date_time_obj < test_date_time_obj:
                    raise ValueError("Results date and time cannot be before the test date and time.")
            except ValueError as ve:
                if "day is out of range for month" in str(ve):
                    raise ValueError("Results date is invalid: day is out of range for month.")
                elif "month must be in 1..12" in str(ve):
                    raise ValueError("Results date is invalid: month must be between 1 and 12.")
                elif "unconverted data remains" in str(ve):
                    raise ValueError("Results date and time must be in the format YYYY-MM-DD hh:mm.")
                else:
                    raise

        # Add to patient records
        if patient_id not in patients:
            patients[patient_id] = Patient(patient_id)

        patient = patients[patient_id]
        test_record = TestRecord(patient_id, test_name, test_date_time, test_result, unit, status,
                                 results_date_time if results_date_time else None)
        patient.add_test_record(test_record)

        # Save the valid medical test record to the file
        with open("medicalRecord.txt", "a") as fo:
            fo.write(f"{patient_id}: {test_name}, {test_date_time}, {test_result}, {unit}, {status.lower()}")
            if results_date_time:
                fo.write(f", {results_date_time}")
            fo.write("\n")

        print(f"Medical test record for '{test_name}' added successfully.")

    except ValueError as ve:
        print(f"Error: {ve}")
    except IOError:
        print("Error: Unable to write to the file. Please check file permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def update_patient_records():
    try:
        # Input Patient ID
        patient_id = input("Enter patient ID (7 digits): ").strip()
        if not patient_id:
            raise ValueError("Patient ID cannot be empty.")
        if not re.match("^\\d{7}$", patient_id):
            raise ValueError("Patient ID must be exactly 7 digits long and contain only numbers.")

        if patient_id not in patients:
            print(f"Patient with ID {patient_id} not found.")
            return

        # Input Test Name
        test_name = input("Enter test name to update: ").strip()
        if not test_name:
            raise ValueError("Test name cannot be empty.")
        if test_name.isdigit():
            raise ValueError("Test name cannot be a number.")
        if not re.match("^[A-Za-z ]+$", test_name):
            raise ValueError("Test name must contain only alphabetic characters and spaces.")

        patient = patients[patient_id]
        for record in patient.get_records():
            if record.test_name == test_name:
                print("Record Found:")
                print(record)
                break
        else:
            print(f"No test record found with the name {test_name} for patient ID {patient_id}.")
            return

        # Input New Test Date and Time
        new_test_date_time = input("Enter new test date and time (YYYY-MM-DD hh:mm): ").strip()
        try:
            new_test_date_time_obj = datetime.strptime(new_test_date_time, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("New test date and time must be in the format YYYY-MM-DD hh:mm.")

        # Input New Test Result
        new_test_result = input("Enter new test result: ").strip()
        if not new_test_result:
            raise ValueError("New test result cannot be empty.")
        if not re.match(r'^-?\d+(\.\d+)?$', new_test_result):
            raise ValueError("New test result must be a valid number.")
        new_test_result = float(new_test_result)

        # Input New Unit of Measurement
        new_unit = input("Enter new unit of measurement (e.g., mg/dL): ").strip()
        if not new_unit:
            raise ValueError("Unit of measurement cannot be empty.")
        if not re.match("^[A-Za-z/]+$", new_unit):
            raise ValueError("Unit of measurement must contain only alphabetic characters and '/'.")

        # Input New Status
        new_status = input("Enter new test status (Pending, Completed, Reviewed): ").strip().capitalize()
        if new_status.isdigit():
            raise ValueError("Status cannot be a number.")
        if new_status not in ["Pending", "Completed", "Reviewed"]:
            raise ValueError("Status must be 'Pending', 'Completed', or 'Reviewed'.")

        # Input New Results Date and Time if status is 'Completed'
        new_results_date_time = ""
        if new_status == "Completed":
            new_results_date_time = input("Enter new results date and time (YYYY-MM-DD hh:mm): ").strip()
            try:
                new_results_date_time_obj = datetime.strptime(new_results_date_time, "%Y-%m-%d %H:%M")
                if new_results_date_time_obj < new_test_date_time_obj:
                    raise ValueError("New results date and time cannot be before the new test date and time.")
            except ValueError as ve:
                if "day is out of range for month" in str(ve):
                    raise ValueError("New results date is invalid: day is out of range for month.")
                elif "month must be in 1..12" in str(ve):
                    raise ValueError("New results date is invalid: month must be between 1 and 12.")
                elif "unconverted data remains" in str(ve):
                    raise ValueError("New results date and time must be in the format YYYY-MM-DD hh:mm.")
                else:
                    raise

        # Update the patient record
        updated_record = TestRecord(patient_id, test_name, new_test_date_time, new_test_result, new_unit, new_status,
                                    new_results_date_time if new_results_date_time else None)
        patient.update_test_record(test_name, updated_record)

        # Rewrite the file with the updated record
        with open("medicalRecord.txt", "r") as fo:
            lines = fo.readlines()

        with open("medicalRecord.txt", "w") as fo:
            for line in lines:
                if line.startswith(f"{patient_id}: {test_name},"):
                    fo.write(
                        f"{patient_id}: {test_name}, {new_test_date_time}, {new_test_result}, {new_unit}, {new_status.lower()}")
                    if new_results_date_time:
                        fo.write(f", {new_results_date_time}")
                    fo.write("\n")
                else:
                    fo.write(line)

        print(f"Test record for '{test_name}' updated successfully.")

    except ValueError as ve:
        print(f"Error: {ve}")
    except IOError:
        print("Error: Unable to write to the file. Please check file permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def search_by_patient_id():
    try:
        patient_id = input("Enter patient ID to search: ").strip()
        found = False
        with open('medicalRecord.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(patient_id):
                    print(line.strip())
                    found = True
        if not found:
            print(f"No records found for Patient ID: {patient_id}")
    except FileNotFoundError:
        print("Error: The medicalRecord.txt file does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




def update_medical_test():
    try:
        # Input Test Name to Update
        old_test_name = input("Enter the test name to update: ").strip()
        if not old_test_name:
            raise ValueError("Test name cannot be empty.")
        if old_test_name.isdigit():
            raise ValueError("Test name cannot be a number.")
        if not re.match("^[A-Za-z ]+$", old_test_name):
            raise ValueError("Test name must contain only alphabetic characters and spaces.")

        # Read all records from the file
        with open("medicalTest.txt", "r") as file:
            lines = file.readlines()

        # Variables to track if the record is found and updated
        updated = False
        updated_lines = []

        for line in lines:
            if line.startswith(f"{old_test_name},"):
                print(f"Updating test '{old_test_name}'")

                # Input new details
                new_name = input(f"Enter new test name (current: {old_test_name}): ").strip()
                if not new_name:
                    raise ValueError("Test name cannot be empty.")
                if new_name.isdigit():
                    raise ValueError("Test name cannot be a number.")
                if not re.match("^[A-Za-z ]+$", new_name):
                    raise ValueError("Test name must contain only alphabetic characters and spaces.")

                new_lower_bound = input("Enter new lower bound for normal range: ").strip()
                if not re.match(r'^-?\d+(\.\d+)?$', new_lower_bound):
                    raise ValueError("Lower bound must be a valid number.")
                new_lower_bound = float(new_lower_bound)

                new_upper_bound = input("Enter new upper bound for normal range: ").strip()
                if not re.match(r'^-?\d+(\.\d+)?$', new_upper_bound):
                    raise ValueError("Upper bound must be a valid number.")
                new_upper_bound = float(new_upper_bound)

                if new_lower_bound >= new_upper_bound:
                    raise ValueError("Lower bound must be less than upper bound.")

                new_unit = input("Enter new unit of the test: ").strip()
                if not new_unit:
                    raise ValueError("Unit cannot be empty.")
                if not re.match("^[A-Za-z ]+$", new_unit):
                    raise ValueError("Unit must contain only alphabetic characters and spaces.")

                new_turnaround_time = input("Enter new turnaround time (DD-hh-mm): ").strip()
                if not re.match(r'^\d{2}-\d{2}-\d{2}$', new_turnaround_time):
                    raise ValueError("Turnaround time must be in the format DD-hh-mm.")

                # Write the updated record
                updated_record = f"{new_name}, {new_lower_bound}, {new_upper_bound}, {new_unit}, {new_turnaround_time}\n"
                updated_lines.append(updated_record)
                updated = True
            else:
                # Keep the original line
                updated_lines.append(line)

        if updated:
            # Write all lines back to the file
            with open("medicalTest.txt", "w") as file:
                file.writelines(updated_lines)
            print(f"Test '{old_test_name}' updated successfully.")
        else:
            print(f"Test '{old_test_name}' not found.")

    except ValueError as ve:
        print(f"Error: {ve}")
    except IOError:
        print("Error: Unable to read/write to the file. Please check file permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def print_all_patients():
    for patient in patients.values():
        print(patient)









def search_by_test_name():
    try:
        # Input Test Name to Search
        test_name = input("Enter test name to search: ").strip()
        if not test_name:
            raise ValueError("Test name cannot be empty.")
        if test_name.isdigit():
            raise ValueError("Test name cannot be a number.")
        if not re.match("^[A-Za-z ]+$", test_name):
            raise ValueError("Test name must contain only alphabetic characters and spaces.")

        results = set()  # Use a set to avoid duplicate entries
        with open('medicalRecord.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if f"{test_name}," in line:
                    results.add(line.strip())

        if results:
            print(f"Records for Test Name '{test_name}':")
            for record in results:
                print(record)
        else:
            print(f"No records found for Test Name: {test_name}")

    except FileNotFoundError:
        print("Error: The medicalRecord.txt file does not exist.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def search_by_test_status():
    try:
        # Input Test Status to Search
        status = input("Enter test status to search (Pending, Completed, Reviewed): ").strip().capitalize()
        if status not in ["Pending", "Completed", "Reviewed"]:
            raise ValueError("Status must be 'Pending', 'Completed', or 'Reviewed'.")

        results = []
        with open('medicalRecord.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if f", {status.lower()}" in line:
                    results.append(line.strip())

        if results:
            print(f"Records with Test Status '{status}':")
            for record in results:
                print(record)
        else:
            print(f"No records found with Test Status: {status}")

    except FileNotFoundError:
        print("Error: The medicalRecord.txt file does not exist.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def search_by_date_range():
    from datetime import datetime

    try:
        # Input Start Date
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Start date must be in the format YYYY-MM-DD.")

        # Input End Date
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        try:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("End date must be in the format YYYY-MM-DD.")

        if start_date_obj > end_date_obj:
            raise ValueError("Start date must be earlier than or equal to the end date.")

        results = []
        with open('medicalRecord.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Extract the test date from the record
                parts = line.split(", ")
                if len(parts) < 2:
                    continue

                # The test date is the second part (format: YYYY-MM-DD hh:mm)
                test_date_str = parts[1]
                try:
                    test_date_obj = datetime.strptime(test_date_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    # Handle cases where the date format is incorrect
                    continue

                # Check if the test date is within the specified range
                if start_date_obj <= test_date_obj <= end_date_obj:
                    results.append(line.strip())

        if results:
            print(f"Records within the date range {start_date} to {end_date}:")
            for record in results:
                print(record)
        else:
            print(f"No records found within the date range {start_date} to {end_date}.")

    except FileNotFoundError:
        print("Error: The medicalRecord.txt file does not exist.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")






def find_abnormal_tests():
    try:
        # Read the test range details from the file
        test_ranges = {}
        with open("medicalTest.txt", "r") as file:
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) >= 4:
                    test_name = parts[0].strip()
                    lower_bound_str = parts[1].strip()
                    upper_bound_str = parts[2].strip()
                    unit = parts[3].strip()

                    # Handle 'Range' or specific values for lower and upper bounds
                    if lower_bound_str.lower() == "range":
                        lower_bound = None
                    else:
                        lower_bound = float(lower_bound_str)

                    if upper_bound_str.lower() == "range":
                        upper_bound = None
                    else:
                        upper_bound = float(upper_bound_str)

                    # Store the details in the dictionary
                    test_ranges[test_name] = {
                        "lower_bound": lower_bound,
                        "upper_bound": upper_bound,
                        "unit": unit
                    }

        print("Test ranges loaded:")
        for test_name, details in test_ranges.items():
            print(f"{test_name}: {details}")

        # Read test records and check for abnormalities
        abnormal_tests = []
        with open("medicalRecord.txt", "r") as file:
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) >= 6:
                    patient_id, test_name, test_datetime, result_value_str, result_unit, status = map(str.strip, parts)
                    patient_id = patient_id.split(":")[1].strip()  # Extract patient_id
                    if test_name in test_ranges:
                        range_info = test_ranges[test_name]
                        try:
                            result_value = float(result_value_str)
                            lower_bound = range_info["lower_bound"]
                            upper_bound = range_info["upper_bound"]

                            # Check if the result is outside the normal range
                            if (lower_bound is not None and result_value < lower_bound) or (
                                    upper_bound is not None and result_value > upper_bound):
                                abnormal_tests.append(line.strip())
                        except ValueError as e:
                            print(
                                f"Error: Could not convert value '{result_value_str}' to float for test '{test_name}': {e}")

        # Print abnormal tests
        if abnormal_tests:
            print("Abnormal test results found:")
            for test in abnormal_tests:
                print(test)
        else:
            print("No abnormal test results found.")

    except FileNotFoundError:
        print("Error: The required file(s) do not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")






def export_medical_records_to_txt():
    try:
        # Open the original medical record file
        with open('medicalRecord.txt', 'r') as infile:
            # Read the lines from the file
            records = infile.readlines()

        # Open a new file to write the data
        with open('exportedMedicalRecords.txt', 'w') as outfile:
            # Optionally write a header or title
            outfile.write("Exported Medical Records\n")
            outfile.write("=" * 30 + "\n\n")  # Decorative separator

            # Write each record to the new text file
            for record in records:
                # Strip any extra spaces or newline characters
                record = record.strip()
                outfile.write(record + '\n')

        print("Medical records have been successfully exported to exportedMedicalRecords.txt.")

    except FileNotFoundError:
        print("Error: The medicalRecord.txt file does not exist.")
    except IOError:
        print("Error: Unable to write to the text file. Please check file permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




def import_medical_records():
    filename = 'medicalRecord.txt'
    records = []
    warnings = []

    def validate_date(date_string):
        # Match date in format YYYY-MM-DD or YYYY-MM-DD HH:MM
        return bool(re.match(r'\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?', date_string))

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            if len(parts) >= 5:  # Expecting at least 5 parts
                try:
                    # Extract and validate components
                    record_id, test_name = parts[0].split(': ')
                    test_date = parts[1]
                    test_result = float(parts[2])  # Convert test result to float
                    test_unit = parts[3]
                    test_status = parts[4]
                    completed_date = parts[5] if len(parts) == 6 and test_status == 'completed' else None

                    # Validate date format
                    if not validate_date(test_date):
                        raise ValueError("Invalid date format in Test Date")
                    if completed_date and not validate_date(completed_date):
                        raise ValueError("Invalid date format in Completed Date")

                    # Store the record
                    record = {
                        'Record ID': record_id,
                        'Test Name': test_name,
                        'Test Date': test_date,
                        'Test Result': test_result,
                        'Test Unit': test_unit,
                        'Test Status': test_status,
                        'Completed Date': completed_date
                    }
                    records.append(record)
                except (ValueError, IndexError) as e:
                    warnings.append(f"Warning: Record format issue in line: {line.strip()}")
            else:
                warnings.append(f"Warning: Record format issue in line: {line.strip()}")

    # Display warnings
    for warning in warnings:
        print(warning)

    print("Medical records have been successfully imported.")

    # Print the imported records
    for record in records:
        print(record)

    return records




def parse_turnaround_time(turnaround_time_str):
    """Parse the turnaround time from a string in format DD-hh-mm."""
    try:
        days, hours, minutes = map(int, turnaround_time_str.split('-'))
        return timedelta(days=days, hours=hours, minutes=minutes)
    except ValueError:
        raise ValueError(f"Invalid turnaround time format: {turnaround_time_str}")

def search_by_turnaround_time_range():
    try:
        # Input Minimum Turnaround Time
        min_turnaround_str = input("Enter minimum turnaround time (DD-hh-mm): ").strip()
        min_turnaround_time = parse_turnaround_time(min_turnaround_str)

        # Input Maximum Turnaround Time
        max_turnaround_str = input("Enter maximum turnaround time (DD-hh-mm): ").strip()
        max_turnaround_time = parse_turnaround_time(max_turnaround_str)

        if min_turnaround_time > max_turnaround_time:
            raise ValueError("Minimum turnaround time must be earlier than or equal to the maximum turnaround time.")

        results = []
        with open('medicalTest.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Extract the parts from the record
                parts = line.split(", ")
                if len(parts) < 5:
                    print(f"Warning: Record format issue in line: {line.strip()}. Error: Not enough parts.")
                    continue

                # Extract the turnaround time from the last part
                turnaround_time_str = parts[-1].strip()

                try:
                    turnaround_time = parse_turnaround_time(turnaround_time_str)
                except ValueError:
                    print(f"Error parsing turnaround time in line: {line.strip()}.")
                    continue

                # Check if the turnaround time is within the specified range
                if min_turnaround_time <= turnaround_time <= max_turnaround_time:
                    results.append(f"Test: {line.strip()}")

        if results:
            print(f"Records with turnaround time within the range {min_turnaround_str} to {max_turnaround_str}:")
            for record in results:
                print(record)
        else:
            print(f"No records found within the specified turnaround time range.")

    except FileNotFoundError:
        print("Error: The medicalTest.txt file does not exist.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def parse_turnaround_time(turnaround_time_str):
    """Parse turnaround time from string in format DD-hh-mm."""
    try:
        days, hours, minutes = map(int, turnaround_time_str.split('-'))
        return timedelta(days=days, hours=hours, minutes=minutes)
    except ValueError:
        raise ValueError(f"Invalid turnaround time format: {turnaround_time_str}")

def calculate_statistics(durations):
    """Calculate minimum, maximum, and average turnaround times."""
    if not durations:
        return None, None, None

    min_duration = min(durations)
    max_duration = max(durations)
    avg_duration = sum(durations, timedelta()) / len(durations)
    return min_duration, max_duration, avg_duration

def generate_turnaround_time_report():
    try:
        # Input minimum and maximum turnaround time
        min_turnaround_str = input("Enter minimum turnaround time (DD-hh-mm): ").strip()
        max_turnaround_str = input("Enter maximum turnaround time (DD-hh-mm): ").strip()

        min_turnaround_time = parse_turnaround_time(min_turnaround_str)
        max_turnaround_time = parse_turnaround_time(max_turnaround_str)

        if min_turnaround_time > max_turnaround_time:
            raise ValueError("Minimum turnaround time must be less than or equal to the maximum turnaround time.")

        turnaround_times = []

        with open('medicalTest.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.split(", ")
                if len(parts) < 5:
                    print(f"Warning: Record format issue in line: {line.strip()}. Error: Not enough parts.")
                    continue

                turnaround_time_str = parts[-1].strip()
                try:
                    turnaround_time = parse_turnaround_time(turnaround_time_str)
                except ValueError:
                    print(f"Error parsing turnaround time in line: {line.strip()}.")
                    continue

                if min_turnaround_time <= turnaround_time <= max_turnaround_time:
                    turnaround_times.append(turnaround_time)

        min_turnaround, max_turnaround, avg_turnaround = calculate_statistics(turnaround_times)

        print(f"Summary Report:")
        if min_turnaround is not None:
            print(f"Minimum Turnaround Time: {min_turnaround}")
            print(f"Maximum Turnaround Time: {max_turnaround}")
            print(f"Average Turnaround Time: {avg_turnaround}")
        else:
            print("No valid turnaround times found within the specified range.")

    except FileNotFoundError:
        print("Error: The medicalTest.txt file does not exist.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")














def display_menu():
    print("\nMedical Test Management System")
    print("1. Add New Medical Test")
    print("2. Add New Medical Record")
    print("3. Update Patient Records")
    print("4. Update Medical Tests")
    print("5. Search by Patient ID")
    print("6. Search by Test Name")
    print("7.  Search for Abnormal Test Results")
    print("8.  Search Tests within a Specific Period")
    print("9. Search by Test Status")
    print("10.  Search by Test Turnaround Time within a Period")
    print("11. Generate Textual Summary Reports")
    print("12. Export Medical Records")
    print("13. Import Medical Records")
    print("14. Exit")


def main():
    while True:
        display_menu()
        choice = input("Please choose an option: ").strip()
        if choice == '1':
            add_new_medical_test()
        elif choice == '2':
            add_new_medical_test_record()
        elif choice == '3':
            update_patient_records()
        elif choice == '4':
            update_medical_test()
        elif choice == '5':
            search_by_patient_id()
        elif choice == '6':
            search_by_test_name()
        elif choice == '8':
            search_by_date_range()
        elif choice == '9':
            search_by_test_status()
        elif choice == '10':
            search_by_turnaround_time_range()
        elif choice == '11':
            generate_turnaround_time_report()
        elif choice == '12':
            export_medical_records_to_txt()
        elif choice == '13':
            import_medical_records()
        elif choice == '14':
            print("Exiting the program...")
            exit(0)
        else:
            print("Invalid choice. Please try again.")





if __name__ == "__main__":
    main()
