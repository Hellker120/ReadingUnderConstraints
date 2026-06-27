def generate_url_list(webname, route, start_no, end_no, file_name):
    # Open the file for writing
    with open(file_name, 'w') as file:
        for i in range(start_no, end_no + 1):
            # Generate the URL in the format: webname/route-1, webname/route-2, ...
            url = f"{webname}{route}-{i}"
            # Write the URL to the file, followed by a comma (except for the last one)
            file.write(url)
            if i < end_no:
                file.write(", ")
            else:
                file.write("\n")  # Newline after the last URL

    print(f"URLs have been written to {file_name}")

# Example usage
if __name__ == "__main__":
    # Take input from the user
    webname = input("Enter the base website name (e.g., https://example.com): ")
    route = input("Enter the route (e.g., /page): ")
    start_no = int(input("Enter the start number (e.g., 1): "))
    end_no = int(input("Enter the end number (e.g., 100): "))
    file_name = input("Enter the output file name (e.g., thisfile.txt): ")

    # Generate the URL list and write it to the file
    generate_url_list(webname, route, start_no, end_no, file_name)