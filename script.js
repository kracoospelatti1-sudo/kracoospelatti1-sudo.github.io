document.addEventListener('DOMContentLoaded', function() {

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Contact form submission
    const contactForm = document.getElementById('contact-form');
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Aquí podrías integrar un servicio como EmailJS o Formspree
        // Por ahora, solo mostramos una alerta y reseteamos el formulario.
        
        const name = this.querySelector('input[name="name"]').value;
        alert(`Gracias por tu mensaje, ${name}. Nos pondremos en contacto pronto.`);
        
        this.reset();
    });

    // --- Lógica del Modal para "Ver Canales" ---
    const modal = document.getElementById("modalCanales");
    const modalImg = document.getElementById("imgModal");
    const btnsVerCanales = document.querySelectorAll(".btn-ver-canales");
    const closeModal = document.querySelector(".close-modal");

    btnsVerCanales.forEach(btn => {
        btn.addEventListener("click", function(e) {
            e.preventDefault(); // Evita que la página salte al inicio
            const imageName = this.getAttribute("data-image");
            modal.style.display = "flex";
            modalImg.src = imageName;
        });
    });

    // Cierra el modal al hacer clic en la 'X'
    closeModal.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Cierra el modal al hacer clic fuera de la imagen
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    // --- Lógica del Acordeón FAQ ---
    const faqItems = document.querySelectorAll(".faq-item");

    faqItems.forEach(item => {
        const question = item.querySelector(".faq-question");
        question.addEventListener("click", () => {
            const currentlyActive = document.querySelector(".faq-item.active");
            if (currentlyActive && currentlyActive !== item) {
                currentlyActive.classList.remove("active");
            }
            item.classList.toggle("active");
        });
    });

});