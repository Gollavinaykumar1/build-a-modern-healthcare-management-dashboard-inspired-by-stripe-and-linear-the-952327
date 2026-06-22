# LLM Output

=== FILE: src/App.jsx ===
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer } from 'react-toastify';
import { Toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { FiUser, FiCalendar, FiClock, FiPlus } from 'react-icons/fi';
import { useForm } from 'react-hook-form';
import { clsx } from 'clsx';
import 'tailwindcss/base.css';
import 'tailwindcss/components.css';
import 'tailwindcss/utilities.css';

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Header() {
  return (
    <div className="bg-gray-800 text-white p-4 flex justify-between">
      <h1 className="text-2xl font-bold">Healthcare Management Dashboard</h1>
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Book Appointment
      </button>
    </div>
  );
}

function Footer() {
  return (
    <div className="bg-gray-800 text-white p-4 text-center">
      &copy; 2024 Healthcare Management Dashboard
    </div>
  );
}

function BookAppointmentForm() {
  const { register, handleSubmit, reset } = useForm();
  const [departments, setDepartments] = useState([
    { id: 1, name: 'General' },
    { id: 2, name: 'Cardiology' },
    { id: 3, name: 'Neurology' },
    { id: 4, name: 'Orthopedics' },
    { id: 5, name: 'Pediatrics' },
  ]);

  const onSubmit = async (data) => {
    try {
      const response = await axios.post(`${BASE_URL}/appointments`, data);
      Toast.success('Appointment booked successfully!');
      reset();
    } catch (error) {
      Toast.error('Error booking appointment!');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="p-4 bg-gray-100 rounded">
      <h2 className="text-lg font-bold mb-4">Book Appointment</h2>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="patientName">
          Patient Name
        </label>
        <input
          {...register('patientName')}
          type="text"
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="doctor">
          Doctor
        </label>
        <input
          {...register('doctor')}
          type="text"
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="department">
          Department
        </label>
        <select
          {...register('department')}
          className="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-2 px-3 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        >
          {departments.map((department) => (
            <option key={department.id} value={department.name}>
              {department.name}
            </option>
          ))}
        </select>
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="date">
          Date
        </label>
        <input
          {...register('date')}
          type="date"
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="time">
          Time
        </label>
        <input
          {...register('time')}
          type="time"
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="notes">
          Notes
        </label>
        <textarea
          {...register('notes')}
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <button
        type="submit"
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Book Appointment
      </button>
    </form>
  );
}

function AppointmentList() {
  const [appointments, setAppointments] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/appointments`);
        const safeList = Array.isArray(response.data) ? response.data : (response.data?.items || []);
        setAppointments(safeList);
      } catch (error) {
        Toast.error('Error fetching appointments!');
      }
    };
    fetchAppointments();
  }, []);

  const filteredAppointments = appointments.filter((appointment) => {
    if (filter === 'all') return true;
    return appointment.department === filter;
  });

  return (
    <div className="p-4 bg-gray-100 rounded">
      <h2 className="text-lg font-bold mb-4">Appointments</h2>
      <div className="mb-4">
        <button
          onClick={() => setFilter('all')}
          className={clsx('bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded', {
            'bg-blue-500 hover:bg-blue-700 text-white': filter === 'all',
          })}
        >
          All
        </button>
        <button
          onClick={() => setFilter('General')}
          className={clsx('bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded', {
            'bg-blue-500 hover:bg-blue-700 text-white': filter === 'General',
          })}
        >
          General
        </button>
        <button
          onClick={() => setFilter('Cardiology')}
          className={clsx('bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded', {
            'bg-blue-500 hover:bg-blue-700 text-white': filter === 'Cardiology',
          })}
        >
          Cardiology
        </button>
        <button
          onClick={() => setFilter('Neurology')}
          className={clsx('bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded', {
            'bg-blue-500 hover:bg-blue-700 text-white': filter === 'Neurology',
          })}
        >
          Neurology
        </button>
        <button
          onClick={() => setFilter('Orthopedics')}
          className={clsx('bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded', {
            'bg-blue-500 hover:bg-blue-700 text-white': filter === 'Orthopedics',
          })}
        >
          Orthopedics
        </button>
        <button
          onClick={() => setFilter('Pediatrics')}
          className={clsx('bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded', {
            'bg-blue-500 hover:bg-blue-700 text-white': filter === 'Pediatrics',
          })}
        >
          Pediatrics
        </button>
      </div>
      <table className="w-full text-left">
        <thead>
          <tr>
            <th className="px-4 py-2">Doctor</th>
            <th className="px-4 py-2">Department</th>
            <th className="px-4 py-2">Date/Time</th>
            <th className="px-4 py-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {filteredAppointments.map((appointment) => (
            <tr key={appointment.id}>
              <td className="px-4 py-2">{appointment.doctor}</td>
              <td className="px-4 py-2">{appointment.department}</td>
              <td className="px-4 py-2">{appointment.date} {appointment.time}</td>
              <td className="px-4 py-2">
                {appointment.status === 'Scheduled' ? (
                  <span className="bg-green-200 text-green-600 py-1 px-2 rounded">
                    Scheduled
                  </span>
                ) : appointment.status === 'Pending' ? (
                  <span className="bg-yellow-200 text-yellow-600 py-1 px-2 rounded">
                    Pending
                  </span>
                ) : (
                  <span className="bg-red-200 text-red-600 py-1 px-2 rounded">
                    Cancelled
                  </span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function MetricCards() {
  const [metrics, setMetrics] = useState({
    totalPatients: 0,
    appointmentsThisMonth: 0,
    revenueGenerated: 0,
    availableDoctors: 0,
  });

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/metrics`);
        setMetrics(response.data);
      } catch (error) {
        Toast.error('Error fetching metrics!');
      }
    };
    fetchMetrics();
  }, []);

  return (
    <div className="flex flex-wrap justify-center">
      <div className="bg-gray-100 rounded p-4 w-full md:w-1/2 xl:w-1/4 mb-4">
        <h2 className="text-lg font-bold mb-2">Total Patients</h2>
        <p className="text-2xl font-bold">{metrics.totalPatients}</p>
      </div>
      <div className="bg-gray-100 rounded p-4 w-full md:w-1/2 xl:w-1/4 mb-4">
        <h2 className="text-lg font-bold mb-2">Appointments This Month</h2>
        <p className="text-2xl font-bold">{metrics.appointmentsThisMonth}</p>
      </div>
      <div className="bg-gray-100 rounded p-4 w-full md:w-1/2 xl:w-1/4 mb-4">
        <h2 className="text-lg font-bold mb-2">Revenue Generated</h2>
        <p className="text-2xl font-bold">${metrics.revenueGenerated}</p>
      </div>
      <div className="bg-gray-100 rounded p-4 w-full md:w-1/2 xl:w-1/4 mb-4">
        <h2 className="text-lg font-bold mb-2">Available Doctors</h2>
        <p className="text-2xl font-bold">{metrics.availableDoctors}</p>
      </div>
    </div>
  );
}

function App() {
  return (
    <HashRouter>
      <Header />
      <Routes>
        <Route
          path="/"
          element={
            <div className="p-4">
              <BookAppointmentForm />
              <AppointmentList />
              <MetricCards />
            </div>
          }
        />
      </Routes>
      <Footer />
      <ToastContainer />
    </HashRouter>
  );
}

export default App;
=== END ===

=== FILE: src/main.jsx ===
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
=== END ===

=== FILE: src/index.css ===
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-gray-100;
}

.container {
  @apply mx-auto p-4;
}
=== END ===

=== FILE: src/api.js ===
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
});

export default api;
=== END ===