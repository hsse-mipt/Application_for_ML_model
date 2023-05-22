//import readFile from '../../../analyzed_news.json' assert {type: "json"}

const negativeNews = document.querySelector(".card__news-negative");
const neutralNews = document.querySelector(".card__news-neutral");
const positiveNews = document.querySelector(".card__news-positive");
const cards = document.querySelector(".cards");

//console.log(readFile);

function updateCard(card, title, text, link, date) {
    const titleElement = card.querySelector(".card__news-title");
    const textElement = card.querySelector(".card__news-text");

    titleElement.textContent = title;
    titleElement.href = link;
    textElement.textContent = text;
}

function makeCard(data) {

    const titles = Object.values(data["title"]);    
    const textes = Object.values(data["description"]);
    const links = Object.values(data["link"]);
    const dates = Object.values(data["pub_date"]);   

    const card = document.querySelector("#card-template").content.cloneNode(true);

    const buttons = card.querySelectorAll(".button");
    const negativeNews = card.querySelector(".card__news-negative");
    const neutralNews = card.querySelector(".card__news-neutral");
    const positiveNews = card.querySelector(".card__news-positive");

    buttons.forEach(function(buttonElement) {
        buttonElement.addEventListener('click', function(evt) {
            buttons.forEach(function(el) {
                if (evt.target === el) {
                    openButton(el)
                } else {
                    closeButton(el);
                }
            })
        if (buttonElement.id === "negative") {
            openNews(negativeNews);
            closeNews(neutralNews);
            closeNews(positiveNews);
        } else if (buttonElement.id === "neutral") {
            openNews(neutralNews);
            closeNews(negativeNews);
            closeNews(positiveNews);
        } else if (buttonElement.id === "positive") {
            openNews(positiveNews);
            closeNews(neutralNews);
            closeNews(negativeNews);
        }
        })
    })
    if (titles.length >= 3) {
        updateCard(negativeNews, titles[0], textes[0], links[0])
        updateCard(neutralNews, titles[1], textes[1], links[1])
        updateCard(positiveNews, titles[2], textes[2], links[2])
    } 
    return card;
}

function addCard(response) {
    const card = makeCard(response);
    cards.append(card);
}

function closeNews(newsElement) {
    newsElement.classList.remove(`${newsElement.classList[0]}_active`);
}

function openNews(newsElement) {
    newsElement.classList.add(`${newsElement.classList[0]}_active`);
}

const buttons = document.querySelectorAll(".button");
const newsTitleInput = document.querySelector(".header__text-input");
const newsEntityChoice = document.querySelector(".header__form-select");

function closeButton(buttonElement) {
    buttonElement.classList.remove(`${buttonElement.classList[0]}_active`);
}

function openButton(buttonElement) {
    buttonElement.classList.add(`${buttonElement.classList[0]}_active`);
}

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

async function postForm() {
    const data = new URLSearchParams(new FormData(headerForm));
    return await fetch("http://127.0.0.1:8000/", {
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        body: data
    })
    .then(function(res) {
        return(res.json());
    })
}

async function getNews() {
    return fetch("http://127.0.0.1:8000/");
}

const headerForm = document.querySelector(".header__form");
headerForm.addEventListener('submit', async function(evt) {
    evt.preventDefault()
    postForm()
        .then(function(res) {
            console.log(res);
            addCard(res);
        })

})
