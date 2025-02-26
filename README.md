# MyWeb Project

MyWeb เป็นเว็บแอปพลิเคชันที่สร้างขึ้นด้วย Flask เพื่อให้ผู้ใช้สามารถแบ่งปันสถานที่ท่องเที่ยว รีวิว และให้คะแนนสถานที่ต่าง ๆ ได้ โดยผู้ใช้สามารถลงทะเบียน, เข้าสู่ระบบ, อัปโหลดรูปโปรไฟล์, เพิ่มสถานที่, เขียนรีวิว และให้คะแนนได้

## Features

- **ระบบผู้ใช้**: ลงทะเบียน, เข้าสู่ระบบ, อัปโหลดรูปโปรไฟล์
- **เพิ่มสถานที่**: ผู้ใช้สามารถเพิ่มสถานที่ท่องเที่ยว พร้อมคำอธิบายและรูปภาพ
- **รีวิวและให้คะแนน**: ผู้ใช้สามารถเขียนรีวิวและให้คะแนนสถานที่ต่าง ๆ
- **แก้ไขและลบสถานที่**: ผู้ใช้สามารถแก้ไขหรือลบสถานที่ที่ตัวเองโพสต์ได้
- **แก้ไขและลบรีวิว**: ผู้ใช้สามารถแก้ไขหรือลบรีวิวที่ตัวเองเขียนได้
- **แสดงผลสถานที่**: แสดงรายการสถานที่พร้อมรูปภาพ, คำอธิบาย, และคะแนนเฉลี่ย
- **ระบบแบ่งหน้า (Pagination)**: แสดงสถานที่แบบแบ่งหน้าเพื่อความสะดวกในการเรียกดู
- **ระบบสิทธิ์การเข้าถึง**: ใช้ Flask-Login และ Flask-SQLAlchemy เพื่อจัดการสิทธิ์ผู้ใช้

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite
- **อื่น ๆ**: WTForms สำหรับการจัดการฟอร์ม, Bcrypt สำหรับการเข้ารหัสรหัสผ่าน

## Installation and Running the Project

### Installation Steps

1. โคลน repository นี้ลงในเครื่องของคุณ:
   ```bash
   git clone https://github.com/teeranon124/myweb.git
   ```

2. สร้าง Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # บน macOS/Linux
   venv\Scripts\activate    # บน Windows  
   ```

3. ติดตั้ง dependencies ที่จำเป็น:
   ```bash
   pip install -r requirements.txt
   ```


### Running the Project

1. รันเซิร์ฟเวอร์ Flask:
   ```bash
   python3 main.py  # บน macOS/Linux
   python main.py   # บน Windows 
   ```

2. เปิดเบราว์เซอร์และไปที่ `http://127.0.0.1:5000/` เพื่อดูเว็บแอปพลิเคชัน

## Project Structure

```
myweb/
├── .gitignore
├── acl.py            # ระบบควบคุมการเข้าถึง (ACL)
├── forms.py          # ฟอร์มต่าง ๆ สำหรับการลงทะเบียน, เข้าสู่ระบบ, อัปโหลดรูป
├── main.py           # ไฟล์หลักของ Flask Application
├── models.py         # โมเดลฐานข้อมูล (SQLAlchemy)
├── README.md         # เอกสารนี้
├── requirements.txt  # รายการ dependencies
├── static/           # ไฟล์ static เช่น CSS, รูปภาพ
└── templates/        # ไฟล์ HTML templates
    ├── base.html     # Template หลัก
    ├── index.html    # หน้าหลักแสดงรายการสถานที่
    ├── login.html    # หน้าเข้าสู่ระบบ
    ├── register.html # หน้าลงทะเบียน
    ├── profile.html  # หน้าโปรไฟล์ผู้ใช้
    ├── upload.html   # หน้าอัปโหลดรูปโปรไฟล์
    ├── create_place.html # หน้าเพิ่มสถานที่
    ├── place_detail.html # หน้าแสดงรายละเอียดสถานที่
    ├── add_review.html   # หน้าเขียนรีวิว
    ├── view_post.html    # หน้าแสดงสถานที่ที่ผู้ใช้โพสต์
    ├── view_review.html  # หน้าแสดงรีวิวที่ผู้ใช้เขียน
    ├── edit_place.html   # หน้าแก้ไขสถานที่
    └── edit_review.html  # หน้าแก้ไขรีวิว
```

## Code Explanation
1. **main.py**
ไฟล์หลักของแอปพลิเคชัน Flask ประกอบด้วย:

- **Routes**: กำหนดเส้นทางต่าง ๆ ของเว็บแอปพลิเคชัน เช่น /, /login, /register, /profile, /create_place, /add_review, /place_detail, /rate_place, /view_review, /view_post, /edit_place, /delete_place, /edit_review, /delete_review
- **Authentication**: ใช้ Flask-Login เพื่อจัดการการเข้าสู่ระบบและสิทธิ์การเข้าถึง
- **File Upload**: จัดการการอัปโหลดรูปภาพโปรไฟล์และรูปภาพสถานที่
- **Pagination**: แสดงรายการสถานที่แบบแบ่งหน้า

2. **models.py**
ไฟล์ที่กำหนดโมเดลฐานข้อมูลโดยใช้ SQLAlchemy ประกอบด้วย:

- **User**: เก็บข้อมูลผู้ใช้ เช่น username, password, profile picture
- **Place**: เก็บข้อมูลสถานที่ เช่น ชื่อ, คำอธิบาย, รูปภาพ, และคะแนนเฉลี่ย
- **Review**: เก็บข้อมูลรีวิวที่ผู้ใช้เขียน
- **Rating**: เก็บข้อมูลคะแนนที่ผู้ใช้ให้กับสถานที่

3. **forms.py**
ไฟล์ที่กำหนดฟอร์มต่าง ๆ โดยใช้ WTForms ประกอบด้วย:

- **LoginForm**: ฟอร์มสำหรับเข้าสู่ระบบ
- **RegisterForm**: ฟอร์มสำหรับลงทะเบียน
- **PlaceForm**: ฟอร์มสำหรับเพิ่มสถานที่
- **ReviewForm**: ฟอร์มสำหรับเขียนรีวิว

4. **acl.py**
ไฟล์ที่จัดการระบบควบคุมการเข้าถึง (Access Control) โดยใช้ Flask-Login และกำหนดบทบาท (roles) ของผู้ใช้


## Usage

1. **ลงทะเบียนและเข้าสู่ระบบ**: ผู้ใช้สามารถลงทะเบียนและเข้าสู่ระบบเพื่อใช้งานฟีเจอร์ต่าง ๆ
2. **เพิ่มสถานที่**: ผู้ใช้ที่เข้าสู่ระบบแล้วสามารถเพิ่มสถานที่ท่องเที่ยว พร้อมรูปภาพและคำอธิบาย
3. **รีวิวและให้คะแนน**: ผู้ใช้สามารถเขียนรีวิวและให้คะแนนสถานที่ต่าง ๆ ได้
4. **แก้ไขและลบสถานที่**: ผู้ใช้สามารถแก้ไขหรือลบสถานที่ที่ตัวเองโพสต์ได้
5. **แก้ไขและลบรีวิว**: ผู้ใช้สามารถแก้ไขหรือลบรีวิวที่ตัวเองเขียนได้
6. **ดูโปรไฟล์**: ผู้ใช้สามารถดูโปรไฟล์ของตัวเองและสถานที่ที่ตัวเองโพสต์หรือรีวิว


## Developer

- **Teeranon** - [GitHub](https://github.com/teeranon124)

## License

โปรเจกต์นี้อยู่ภายใต้สัญญาอนุญาต MIT ดูไฟล์ [LICENSE](LICENSE) สำหรับรายละเอียดเพิ่มเติม

