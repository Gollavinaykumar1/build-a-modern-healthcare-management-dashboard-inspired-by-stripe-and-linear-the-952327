# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, Patient, Doctor, Appointment

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class PatientData(BaseModel):
    name: str
    email: str

class DoctorData(BaseModel):
    name: str
    specialty: str

class AppointmentData(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    time: str

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Patient).filter(Patient.email == username).first()
    if not user:
        return False
    if not verify_password(password, user.email):
        return False
    return user

def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_db().query(Patient).filter(Patient.email == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(get_db(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/patients/")
async def read_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@app.post("/patients/")
async def create_patient(patient: PatientData, db: Session = Depends(get_db)):
    db_patient = Patient(name=patient.name, email=patient.email)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/doctors/")
async def read_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()

@app.post("/doctors/")
async def create_doctor(doctor: DoctorData, db: Session = Depends(get_db)):
    db_doctor = Doctor(name=doctor.name, specialty=doctor.specialty)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@app.get("/appointments/")
async def read_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@app.post("/appointments/")
async def create_appointment(appointment: AppointmentData, db: Session = Depends(get_db)):
    db_appointment = Appointment(patient_id=appointment.patient_id, doctor_id=appointment.doctor_id, date=appointment.date, time=appointment.time)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@app.post("/book-appointment/")
async def book_appointment(appointment: AppointmentData, db: Session = Depends(get_db)):
    db_appointment = Appointment(patient_id=appointment.patient_id, doctor_id=appointment.doctor_id, date=appointment.date, time=appointment.time)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@app.get("/metrics/")
async def read_metrics(db: Session = Depends(get_db)):
    total_patients = db.query(Patient).count()
    appointments_this_month = db.query(Appointment).filter(Appointment.date >= datetime.now() - timedelta(days=30)).count()
    revenue_generated = 100 * appointments_this_month
    available_doctors = db.query(Doctor).count()
    return {
        "total_patients": total_patients,
        "appointments_this_month": appointments_this_month,
        "revenue_generated": revenue_generated,
        "available_doctors": available_doctors
    }