document.addEventListener("DOMContentLoaded", () => {
  console.log("Скрипт завантажено");

  const modal = document.getElementById("modal");
  const successModal = document.getElementById("successModal");
  const calendarEl = document.getElementById("events-calendar");

  let calendar = null;
  if (window.FullCalendar && calendarEl) {
    calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: "dayGridMonth",
      locale: "uk",
      events: [],
      height: "auto",
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek"
      }
    });
    calendar.render();
  } else {
    console.warn("FullCalendar не завантажено або немає контейнера #events-calendar");
  }

  // Завантажити події з API
  fetch("http://127.0.0.1:8000/api/events/")
    .then(res => res.json())
    .then(data => {
      data.forEach((event, index) => {
        addToTable(event, index + 1);
        if (calendar) {
          calendar.addEvent({
            title: event.text,
            start: `${event.date}T${event.time}`
          });
        }
      });
    })
    .catch(err => console.error("Помилка завантаження подій:", err));

  // Відкрити модальне вікно
  document.getElementById("btn-create")?.addEventListener("click", () => {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  });

  // Надіслати форму
  document.getElementById("event-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    formData.set("is_sent", form.is_sent.checked);
    formData.set("added_to_calendar", form.added_to_calendar.checked);

    fetch("http://127.0.0.1:8000/api/events/create/", {
      method: "POST",
      body: formData
    })
      .then(res => {
        if (!res.ok) throw new Error("Помилка створення події");
        return res.json();
      })
      .then(data => {
        addToTable(data);
        if (calendar) {
          calendar.addEvent({
            title: data.text,
            start: `${data.date}T${data.time}`
          });
        }
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        showSuccess();
        form.reset();
      })
      .catch(err => {
        console.error(err);
        alert("Не вдалося створити подію");
      });
  });

  // Перемикання вкладок
  document.getElementById("btn-table")?.addEventListener("click", () => {
    document.getElementById("tableView").classList.remove("hidden");
    document.getElementById("calendarView").classList.add("hidden");
    setActiveTab("btn-table");
  });

  document.getElementById("btn-calendar")?.addEventListener("click", () => {
    document.getElementById("calendarView").classList.remove("hidden");
    document.getElementById("tableView").classList.add("hidden");
    setActiveTab("btn-calendar");
  });

  // Пошук
  document.querySelector("input[placeholder='Пошук...']")?.addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase();
    document.querySelectorAll("#eventTableBody tr").forEach(row => {
      const text = row.innerText.toLowerCase();
      row.style.display = text.includes(query) ? "" : "none";
    });
  });

  // Мова календаря
  document.getElementById("languageSelect")?.addEventListener("change", (e) => {
    if (calendar) {
      calendar.setOption("locale", e.target.value);
    }
  });

  // Telegram заглушка
  document.getElementById("btn-telegram")?.addEventListener("click", () => {
    alert("Імпорт із Telegram не реалізовано");
  });

  function addToTable(event, index = null) {
    const tbody = document.getElementById("eventTableBody");
    const row = document.createElement("tr");
    row.innerHTML = `
      <td class="p-2">${index ?? "—"}</td>
      <td class="p-2">${event.text}</td>
      <td class="p-2">${event.date}</td>
      <td class="p-2">${event.time}</td>
      <td class="p-2">${event.location || "—"}</td>
      <td class="p-2">${event.is_sent ? "Надіслано" : "Очікує"}</td>
      <td class="p-2 flex gap-2">
        <button class="text-red-400 hover:text-red-600" onclick="deleteEvent(${event.id}, this)">Видалити</button>
        <button class="text-green-400 hover:text-green-600" onclick="markCalendar(${event.id}, this)">+Календар</button>
      </td>
    `;
    tbody.appendChild(row);
  }

  window.deleteEvent = function (id, btn) {
    if (!confirm("Видалити подію?")) return;
    fetch(`http://127.0.0.1:8000/api/events/${id}/delete/`, {
      method: "DELETE"
    })
      .then(res => {
        if (!res.ok) throw new Error("Помилка видалення");
        btn.closest("tr").remove();
      })
      .catch(err => {
        console.error(err);
        alert("Не вдалося видалити подію");
      });
  };

  window.markCalendar = function (id, btn) {
    fetch(`http://127.0.0.1:8000/api/events/${id}/`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ added_to_calendar: true })
    })
      .then(res => {
        if (!res.ok) throw new Error("Помилка оновлення");
        btn.textContent = "✓";
        btn.disabled = true;
      })
      .catch(err => {
        console.error(err);
        alert("Не вдалося оновити подію");
      });
  };

  function showSuccess() {
    successModal.classList.remove("hidden");
    successModal.classList.add("flex");
    setTimeout(() => {
      successModal.classList.add("hidden");
      successModal.classList.remove("flex");
    }, 2000);
  }

  function setActiveTab(id) {
    document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active-tab"));
    document.getElementById(id)?.classList.add("active-tab");
  }
});
