document.addEventListener("DOMContentLoaded", () => {

    const card = document.querySelector(".card");

    if(card){

        card.style.transition = "transform .3s ease, box-shadow .3s ease";

        document.addEventListener("mousemove",(e)=>{

            const rect = card.getBoundingClientRect();

            const x = e.clientX - rect.left;

            const y = e.clientY - rect.top;

            const rotateY = ((x / rect.width) - 0.5) * 16;

            const rotateX = ((rect.height / 2 - y) / rect.height) * 16;

            card.style.transform =
                `perspective(1000px)
                 rotateX(${rotateX}deg)
                 rotateY(${rotateY}deg)
                 scale(1.02)`;

        });

        document.addEventListener("mouseleave",()=>{

            card.style.transform =
                "perspective(1000px) rotateX(0deg) rotateY(0deg)";

        });

    }

});