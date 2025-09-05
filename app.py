import csv
import time
from concurrent.futures import ProcessPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def login_and_sum(data):
    start_time = time.time()


    name = data['NAME']
    username = data['USERNAME']
    password = data['PASSWORD']

    options = Options()
    options.add_argument("--headless")  # run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1280x800")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get("https://studentportalsis.azu.edu.eg/Default.aspx")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtUsername"))
        )
        driver.find_element(By.ID, "txtUsername").send_keys(username)
        driver.find_element(By.ID, "txtPassword").send_keys(password)
        driver.find_element(By.ID, "btnEnter").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_cntphmaster_StudDataGeneralControl1_lblStud"))
        )

        driver.get("https://studentportalsis.azu.edu.eg/UI/StudentView/student_sem_work_Modular.aspx")

        result = { 'NAME': name, "TOTAL 14": 0, "TOTAL 15": 0 }
        
        for year in ["14", "15"]:
            year_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ctl00_cntphmaster_ACadYearDropDownList"))
            )
            Select(year_dropdown).select_by_value(year)
            for semester in ["1", "2"]:
                semester_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ctl00_cntphmaster_semesterDropDownList"))
                )
                Select(semester_dropdown).select_by_value(semester)
                
                driver.find_element(By.ID, "ctl00_cntphmaster_searchButton").click()

                time.sleep(3)

                table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ctl00_cntphmaster_GridView1"))
                )
                rows = table.find_elements(By.TAG_NAME, "tr")[1:]
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 4:
                        try:
                            grade = float(cols[3].text.strip())
                            result[f'TOTAL {year}'] += grade
                        except ValueError:
                            continue

        duration = time.time() - start_time
        print(f"[✅] Done: {name} ({username}) | 🧮 Total 14: {result['TOTAL 14']:.2f} | 🧮 Total 15: {result['TOTAL 15']:.2f} | ⏱️ {duration:.1f}s\n")

        return result

    except Exception as e:
        duration = time.time() - start_time
        print(f"[❌] Error: {name} ({username}) | ⏱️ {duration:.1f}s | Error: {e}")
        driver.save_screenshot(f"{name}_debug.png")
        return None

    finally:
        driver.quit()


def process_students(input_file, output_file, max_workers=4):
    global_start = time.time()
    with open(input_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        students = list(reader)

    results = []
    print(f"🚀 Starting batch for {len(students)} students using {max_workers} workers ...\n")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for result in executor.map(login_and_sum, students):
            if result:
                results.append(result)

    results.sort(key=lambda x: x['TOTAL 14'] + x['TOTAL 15'], reverse=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if len(results) > 0:    
            writer = csv.DictWriter(f, fieldnames=set(key for obj in results for key in obj.keys()))
            writer.writeheader()
            writer.writerows(results)

    print(f"\n🏁 {len(results)} students done in {time.time() - global_start:.1f}s. ✅ Output saved to '{output_file}'")


if __name__ == "__main__":
    process_students("input.csv", "output.csv", max_workers=10)
