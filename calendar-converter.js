// Calendar System Definitions
const calendarSystems = [
    {
        id: 'julian',
        name: 'Julian',
        convert: (date) => {
            const jd = gregorianToJulian(date);
            const months = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];
            return `${jd.day} ${months[jd.month - 1]} ${jd.year}`;
        }
    },
    {
        id: 'japanese',
        name: 'Japanese',
        convert: (date) => {
            const imp = gregorianToJapanese(date);
            return `${imp.era} ${imp.year}, ${date.toLocaleDateString('en-GB', { month: 'long', day: 'numeric' })}`;
        }
    },
    {
        id: 'french',
        name: 'French Republican',
        convert: (date) => {
            const fr = gregorianToFrenchRepublican(date);
            if (fr.dayName) return fr.dayName;
            return `${fr.day} ${fr.month}, Year ${fr.year}`;
        }
    },
    {
        id: 'old-english',
        name: 'Old English',
        convert: (date) => {
            const oe = gregorianToOldEnglish(date);
            return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }).replace(date.getFullYear().toString(), oe.year.toString());
        }
    },
    {
        id: 'american',
        name: 'American Patriotic',
        convert: (date) => {
            const am = gregorianToAmericanPatriotic(date);
            return `${date.toLocaleDateString('en-GB', { day: 'numeric', month: 'long' })}, Year of Liberty ${am.year}`;
        }
    },
    {
        id: 'regnal',
        name: 'British Regnal',
        convert: (date) => {
            const reg = gregorianToRegnal(date);
            return `${reg.regnalYear} ${reg.monarch} (${date.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })})`;
        }
    },
    {
        id: 'babylonian',
        name: 'Babylonian',
        convert: (date) => {
            const bab = gregorianToBabylonian(date);
            return `${bab.day} ${bab.month}, ${bab.year}`;
        }
    },
    {
        id: 'hebrew',
        name: 'Hebrew',
        convert: (date) => {
            const heb = gregorianToHebrew(date);
            return `${heb.day} ${heb.month} ${heb.year}`;
        }
    },
    {
        id: 'islamic',
        name: 'Islamic (Hijri)',
        convert: (date) => {
            const isl = gregorianToIslamic(date);
            return `${isl.day} ${isl.month} ${isl.year} AH`;
        }
    },
    {
        id: 'persian',
        name: 'Persian (Solar Hijri)',
        convert: (date) => {
            const per = gregorianToPersian(date);
            return `${per.day} ${per.month} ${per.year}`;
        }
    },
    {
        id: 'ethiopian',
        name: 'Ethiopian',
        convert: (date) => {
            const eth = gregorianToEthiopian(date);
            return `${eth.day} ${eth.month} ${eth.year}`;
        }
    },
    {
        id: 'chinese',
        name: 'Chinese',
        convert: (date) => {
            const chi = gregorianToChinese(date);
            return `${chi.cyclicalYear}, ${chi.month} ${chi.day}`;
        }
    },
    {
        id: 'unix',
        name: 'Unix Timestamp',
        convert: (date) => {
            return Math.floor(date.getTime() / 1000).toString();
        }
    },
    {
        id: 'iso-week',
        name: 'ISO Week Date',
        convert: (date) => {
            const iso = gregorianToISOWeek(date);
            return `${iso.year}-W${String(iso.week).padStart(2, '0')}-${iso.day}`;
        }
    }
];

// Conversion Functions

function gregorianToJulian(date) {
    const offset = 13;
    const julianDate = new Date(date);
    julianDate.setDate(julianDate.getDate() - offset);
    return {
        year: julianDate.getFullYear(),
        month: julianDate.getMonth() + 1,
        day: julianDate.getDate()
    };
}

function gregorianToJapanese(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();

    if (year > 2019 || (year === 2019 && month >= 5)) {
        return { era: '令和', year: year - 2018 };
    } else if (year > 1989 || (year === 1989 && month >= 1 && day >= 8)) {
        return { era: '平成', year: year - 1988 };
    } else if (year >= 1926) {
        return { era: '昭和', year: year - 1925 };
    }
    return { era: '昭和', year: year - 1925 };
}

function gregorianToFrenchRepublican(date) {
    const months = [
        'Vendémiaire', 'Brumaire', 'Frimaire',
        'Nivôse', 'Pluviôse', 'Ventôse',
        'Germinal', 'Floréal', 'Prairial',
        'Messidor', 'Thermidor', 'Fructidor'
    ];

    const epoch = new Date(1792, 8, 22);
    const diffDays = Math.floor((date - epoch) / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
        return { dayName: 'Before the Revolution' };
    }

    const year = Math.floor(diffDays / 365) + 1;
    const dayOfYear = diffDays % 365;
    const monthIndex = Math.floor(dayOfYear / 30);
    const dayOfMonth = (dayOfYear % 30) + 1;

    if (monthIndex >= 12) {
        return { year, month: 'Sansculottides', day: dayOfYear - 359 };
    }

    return { year, month: months[monthIndex], day: dayOfMonth, dayName: null };
}

function gregorianToOldEnglish(date) {
    const month = date.getMonth() + 1;
    const day = date.getDate();
    let year = date.getFullYear();

    if (month < 3 || (month === 3 && day < 25)) {
        year -= 1;
    }

    return { year };
}

function gregorianToAmericanPatriotic(date) {
    const month = date.getMonth() + 1;
    const day = date.getDate();
    let year = date.getFullYear();

    if (month < 7 || (month === 7 && day < 4)) {
        year -= 1;
    }

    return { year };
}

function gregorianToRegnal(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();

    if (year > 2022 || (year === 2022 && month >= 9 && day >= 8)) {
        const yearsDiff = date.getFullYear() - 2022;
        const regnalYear = (month >= 9 && day >= 8) ? yearsDiff + 1 : yearsDiff;
        return { monarch: 'Charles III', regnalYear: regnalYear };
    } else if (year >= 1952) {
        const yearsDiff = date.getFullYear() - 1952;
        const regnalYear = (month >= 2 && day >= 6) ? yearsDiff + 1 : yearsDiff;
        return { monarch: 'Elizabeth II', regnalYear: regnalYear };
    }

    return { monarch: 'George VI', regnalYear: 1 };
}

function gregorianToBabylonian(date) {
    const months = [
        'Nisanu', 'Ayaru', 'Simanu', 'Du\'uzu',
        'Abu', 'Ululu', 'Tashritu', 'Arakhsamna',
        'Kislimu', 'Tebetu', 'Shabatu', 'Adaru'
    ];

    const month = date.getMonth();
    const babylonianMonth = (month + 9) % 12;
    const year = date.getFullYear() + 3760;

    return { year, month: months[babylonianMonth], day: date.getDate() };
}

function gregorianToHebrew(date) {
    // Simplified approximation
    const months = [
        'Nisan', 'Iyar', 'Sivan', 'Tammuz', 'Av', 'Elul',
        'Tishrei', 'Cheshvan', 'Kislev', 'Tevet', 'Shevat', 'Adar'
    ];

    const hebrewYear = date.getFullYear() + 3760;
    const monthIndex = (date.getMonth() + 6) % 12;

    return {
        day: date.getDate(),
        month: months[monthIndex],
        year: hebrewYear
    };
}

function gregorianToIslamic(date) {
    // Simplified approximation (Islamic calendar is purely lunar)
    const months = [
        'Muharram', 'Safar', 'Rabi\' al-awwal', 'Rabi\' al-thani',
        'Jumada al-awwal', 'Jumada al-thani', 'Rajab', 'Sha\'ban',
        'Ramadan', 'Shawwal', 'Dhu al-Qi\'dah', 'Dhu al-Hijjah'
    ];

    // Simple approximation: Islamic year is about 354 days
    const gregorianEpoch = new Date(622, 6, 16); // Hijra
    const daysSinceEpoch = Math.floor((date - gregorianEpoch) / (1000 * 60 * 60 * 24));
    const islamicYear = Math.floor(daysSinceEpoch / 354) + 1;
    const dayOfYear = daysSinceEpoch % 354;
    const monthIndex = Math.floor(dayOfYear / 29.5);
    const dayOfMonth = Math.floor(dayOfYear % 29.5) + 1;

    return {
        day: dayOfMonth,
        month: months[Math.min(monthIndex, 11)],
        year: islamicYear
    };
}

function gregorianToPersian(date) {
    const months = [
        'Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar',
        'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand'
    ];

    // Simplified: Persian new year is around March 21
    let persianYear = date.getFullYear() - 621;
    const month = date.getMonth();
    const day = date.getDate();

    if (month < 2 || (month === 2 && day < 21)) {
        persianYear -= 1;
    }

    const monthIndex = month >= 2 ? (month - 2) : (month + 10);

    return {
        day: date.getDate(),
        month: months[monthIndex],
        year: persianYear
    };
}

function gregorianToEthiopian(date) {
    const months = [
        'Meskerem', 'Tekemt', 'Hedar', 'Tahsas', 'Ter', 'Yekatit',
        'Megabit', 'Miazia', 'Genbot', 'Sene', 'Hamle', 'Nehasse', 'Pagumen'
    ];

    // Ethiopian calendar is about 7-8 years behind
    const ethiopianYear = date.getFullYear() - 7;
    const monthIndex = (date.getMonth() + 4) % 13;

    return {
        day: date.getDate(),
        month: months[monthIndex],
        year: ethiopianYear
    };
}

function gregorianToChinese(date) {
    // Simplified Chinese calendar representation
    const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
    const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
    const animals = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig'];

    // Year calculation (simplified, Chinese New Year varies)
    const yearOffset = date.getFullYear() - 1984; // 1984 was Year of the Rat (甲子)
    const stemIndex = yearOffset % 10;
    const branchIndex = yearOffset % 12;
    const animal = animals[branchIndex];

    return {
        cyclicalYear: `${stems[stemIndex]}${branches[branchIndex]} (${animal})`,
        month: `Month ${date.getMonth() + 1}`,
        day: `Day ${date.getDate()}`
    };
}

function gregorianToISOWeek(date) {
    const thurs = new Date(date);
    thurs.setDate(date.getDate() + (4 - (date.getDay() || 7)));
    const yearStart = new Date(thurs.getFullYear(), 0, 1);
    const weekNo = Math.ceil((((thurs - yearStart) / 86400000) + 1) / 7);

    return {
        year: thurs.getFullYear(),
        week: weekNo,
        day: date.getDay() || 7
    };
}

// UI State
let currentDate = new Date();

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const dateInput = document.getElementById('date-input');
    dateInput.valueAsDate = currentDate;

    updateDisplay();

    document.getElementById('today-btn').addEventListener('click', setToday);
    dateInput.addEventListener('change', (e) => {
        currentDate = e.target.valueAsDate || new Date();
        updateDisplay();
    });
});

function updateDisplay() {
    // Main date display
    const mainDate = document.getElementById('main-date');
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    mainDate.innerHTML = `
        <div class="date-value">${currentDate.toLocaleDateString('en-GB', options)}</div>
        <div class="day-name">Gregorian Calendar</div>
    `;

    // Calendars list
    const calendarsList = document.getElementById('calendars-list');
    calendarsList.innerHTML = calendarSystems.map(cal => `
        <div class="calendar-item">
            <div class="calendar-name">${cal.name}</div>
            <div class="calendar-value">${cal.convert(currentDate)}</div>
        </div>
    `).join('');
}

function setToday() {
    currentDate = new Date();
    document.getElementById('date-input').valueAsDate = currentDate;
    updateDisplay();
}
