import requests

def test_url(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False
def select_unit():
    print("Select the unit of measurement:")
    print("1. Mbps")
    print("2. Gbps")
    print("3. Kbps")
    choice = input("Enter your choice (1/2/3): ")
    if choice == '1':
        return "Mbps"
    elif choice == '2':
        return "Gbps"
    elif choice == '3':
        return "Kbps"
    else:
        print("Invalid choice. Defaulting to Mbps.")
        return "Mbps"
def create_xml(url):
    name=str(input("Enter the name of the Host: "))
    speed=str(input("Enter the speed without unit of the connection: "))
    unit=select_unit()
    city=str(input("Enter the city: "))
    country=str(input("Enter the country: "))
    country_code=str(input("Enter the country code: "))
    # XML content creation
    xml_name=f"{name}_{speed}{unit}_{city}_{country_code}.xml"
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?><config>
  <test>
    <cases>
      <case>
        <type>get-http</type>
        <name>{name} ({speed}{unit}, {city}, {country})</name>
        <enabled>true</enabled>
        <url>{url}</url>
        <repeat>2</repeat>
        <duration>60</duration>
        <pause>10</pause>
        <concurrence>1</concurrence>
      </case>
    </cases>
  </test>
</config>"""
    # Save the XML content to a file
    with open(xml_name, 'w') as xml_file:
        xml_file.write(xml_content)
def main():
    # Nperf URL
    nperf_url = str(input("Enter the Nperf Domain: "))
    possible_ports_if_failed = [8443]
    # URL Creation:
    url = f"{nperf_url}/1GiB.dat"
    # Test the URL
    if test_url(url):
        create_xml(url)
    else:
        print(f"URL {url} is not reachable. Trying with possible ports...")
        for port in possible_ports_if_failed:
            url = f"{nperf_url}:{port}/1GiB.dat"
            print(f"Trying URL: {url}")
            if test_url(url):
                create_xml(url)
                break
        else:
            print("All attempts to reach the URL failed.")

if __name__ == "__main__":
    main()