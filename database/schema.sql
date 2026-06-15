CREATE TABLE clinics (
    id SERIAL PRIMARY KEY,
    clinic_name VARCHAR(255) NOT NULL,
    owner_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    timezone VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'clinic_owner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    consultation_fee DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE doctor_availability (
    id SERIAL PRIMARY KEY,
    doctor_id INT REFERENCES doctors(id) ON DELETE CASCADE,
    day_of_week VARCHAR(20),
    start_time TIME,
    end_time TIME,
    slot_duration INT DEFAULT 30,
    is_available BOOLEAN DEFAULT true
);

CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    service_name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    duration INT NOT NULL,
    price DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    dob DATE,
    gender VARCHAR(50),
    address TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    doctor_id INT REFERENCES doctors(id) ON DELETE SET NULL,
    patient_id INT REFERENCES patients(id) ON DELETE CASCADE,
    service_id INT REFERENCES services(id) ON DELETE SET NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'unpaid',
    notes TEXT,
    created_by VARCHAR(50) DEFAULT 'ai_agent',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ai_agents (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    agent_name VARCHAR(255) NOT NULL,
    agent_type VARCHAR(100),
    voice VARCHAR(100),
    tone VARCHAR(100),
    sensitivity VARCHAR(50),
    greeting_message TEXT,
    system_prompt TEXT,
    status VARCHAR(50) DEFAULT 'inactive',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE calls (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    patient_id INT REFERENCES patients(id) ON DELETE SET NULL,
    agent_id INT REFERENCES ai_agents(id) ON DELETE SET NULL,
    call_type VARCHAR(50) DEFAULT 'web_voice',
    duration_seconds INT DEFAULT 0,
    call_status VARCHAR(50),
    booking_result VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transcripts (
    id SERIAL PRIMARY KEY,
    call_id INT REFERENCES calls(id) ON DELETE CASCADE,
    speaker VARCHAR(50),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    patient_id INT REFERENCES patients(id) ON DELETE CASCADE,
    appointment_id INT REFERENCES appointments(id) ON DELETE CASCADE,
    amount DECIMAL(10,2),
    payment_method VARCHAR(100),
    payment_status VARCHAR(50) DEFAULT 'pending',
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE support_tickets (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    patient_id INT REFERENCES patients(id) ON DELETE CASCADE,
    subject VARCHAR(255),
    status VARCHAR(50) DEFAULT 'open',
    priority VARCHAR(50) DEFAULT 'normal',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE support_messages (
    id SERIAL PRIMARY KEY,
    ticket_id INT REFERENCES support_tickets(id) ON DELETE CASCADE,
    sender_type VARCHAR(50),
    message TEXT,
    attachment_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE widgets (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    agent_id INT REFERENCES ai_agents(id) ON DELETE SET NULL,
    theme VARCHAR(50) DEFAULT 'light',
    position VARCHAR(50) DEFAULT 'bottom_right',
    greeting TEXT,
    widget_code TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE website_settings (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    template_name VARCHAR(100),
    primary_color VARCHAR(50),
    secondary_color VARCHAR(50),
    logo_url TEXT,
    domain VARCHAR(255),
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE website_pages (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    page_name VARCHAR(100),
    slug VARCHAR(100),
    content JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(255),
    message TEXT,
    type VARCHAR(100),
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    event_name VARCHAR(255),
    event_type VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE plans (
    id SERIAL PRIMARY KEY,
    plan_name VARCHAR(100),
    monthly_price DECIMAL(10,2),
    max_agents INT,
    max_calls INT,
    max_doctors INT,
    website_builder BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clinic_subscriptions (
    id SERIAL PRIMARY KEY,
    clinic_id INT REFERENCES clinics(id) ON DELETE CASCADE,
    plan_id INT REFERENCES plans(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'active',
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);