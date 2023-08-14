//References
let timeLeft = document.querySelector(".time-left");
let quizContainer = document.getElementById("container");
let nextBtn = document.getElementById("next-button");
let countOfQuestion = document.querySelector(".number-of-question");
let displayContainer = document.getElementById("display-container");
let scoreContainer = document.querySelector(".score-container");
let restart = document.getElementById("restart");
let userScore = document.getElementById("user-score");
let userScoreMessage = document.getElementById("user-score-message");
let startScreen = document.querySelector(".start-screen");
let startButton = document.getElementById("start-button");
const homeButton = document.getElementById("home");
let questionCount;
let scoreCount = 0;
let count = 11;
let countdown;
const userEmail = document.getElementById("userEmail").value;
const userUniverse = document.getElementById("userUniverse").value;

let questionsDiv = document.getElementById('my-div');
let questions = questionsDiv.getAttribute('questions');

// console.log(questions)
// const quizArray = questions
const quizArray = JSON.parse(questions);
console.log(quizArray)


function storeUserScore(email, universe, score) {
    $.ajax({
        type: "POST",
        url: "/store_score",
        data: {
            email: email,
            universe: universe,
            score: score
        },
        success: function (response) {
            console.log("Score stored successfully!");
        },
        error: function (error) {
            console.error("Error storing score:", error);
        }
    });
}

homeButton.addEventListener("click", () => {
    window.location.href = "/home";
});

//Restart Quiz
restart.addEventListener("click", () => {
    initial();
    displayContainer.classList.remove("hide");
    scoreContainer.classList.add("hide");
    homeButton.classList.add("hide");
});

//Next Button
nextBtn.addEventListener(
    "click",
    (displayNext = () => {
        //increment questionCount
        questionCount += 1;
        //if last question
        if (questionCount === quizArray.length) {
            //hide question container and display score
            displayContainer.classList.add("hide");
            scoreContainer.classList.remove("hide");
            homeButton.classList.remove("hide");


            let postQuizMessage = '';

            if (scoreCount < 3) {
                postQuizMessage = "Please Try Again!";
            } else if (scoreCount === 3) {
                postQuizMessage = "Good Job!";
                restart.style.display = "none";
            } else if (scoreCount === 4) {
                postQuizMessage = "Excellent Work!";
                restart.style.display = "none";
            } else {
                postQuizMessage = "You are a genius!";
                restart.style.display = "none";
            }
            userScore.innerHTML = "Your score is: " + ((scoreCount / questionCount) * 100) + "%";
            userScoreMessage.innerHTML = postQuizMessage;
            storeUserScore(userEmail, userUniverse, scoreCount);
        } else {
            //display questionCount
            countOfQuestion.innerHTML =
                questionCount + 1 + " of " + quizArray.length + " Question";
            //display quiz
            quizDisplay(questionCount);
            count = 11;
            clearInterval(countdown);
            timerDisplay();
        }
    })
);

//Timer
const timerDisplay = () => {
    countdown = setInterval(() => {
        count--;
        timeLeft.innerHTML = `${count}s`;
        if (count === 0) {
            clearInterval(countdown);
            displayNext();
        }
    }, 1000);
};

//Display quiz
const quizDisplay = (questionCount) => {
    let quizCards = document.querySelectorAll(".container-mid");
    //Hide other cards
    quizCards.forEach((card) => {
        card.classList.add("hide");
    });
    //display current question card
    quizCards[questionCount].classList.remove("hide");
};

//Quiz Creation
function quizCreator() {
    //randomly sort questions
    console.log(quizArray)
    quizArray.sort(() => Math.random() - 0.5);

    //generate quiz
    for (let i of quizArray) {
        //randomly sort options
        const options = [
            i['option_a'],
            i['option_b'],
            i['option_c'],
            i['option_d'],
        ];
        //i.options.sort(() => Math.random() - 0.5);
        for (let j = options.length - 1; j > 0; j--) {
            const k = Math.floor(Math.random() * (j + 1));
            [options[j], options[k]] = [options[k], options[j]];
        }

        //quiz card creation
        let div = document.createElement("div");
        div.classList.add("container-mid", "hide");
        //question number
        countOfQuestion.innerHTML = 1 + " of " + quizArray.length + " Question";
        //question
        let question_DIV = document.createElement("p");
        question_DIV.classList.add("question");
        question_DIV.innerHTML = i.question;
        div.appendChild(question_DIV);
        //options
        div.innerHTML += `
            <button class="option-div" onclick="checker(this)">${options[0]}</button>
            <button class="option-div" onclick="checker(this)">${options[1]}</button>
            <button class="option-div" onclick="checker(this)">${options[2]}</button>
            <button class="option-div" onclick="checker(this)">${options[3]}</button>
        `;
        quizContainer.appendChild(div);
    }
}

//Checker Function to check if option is correct or not
// function checker(userOption) {
//     let userSolution = userOption.innerText;
//     let question =
//         document.getElementsByClassName("container-mid")[questionCount];
//     let options = question.querySelectorAll(".option-div");
//
//     //if user clicked answer == correct option stored in object
//     if (userSolution === quizArray[questionCount].correct_answer) {
//         userOption.classList.add("correct");
//         scoreCount++;
//     } else {
//         userOption.classList.add("incorrect");
//         //For marking the correct option
//         options.forEach((element) => {
//             if (element.innerText === quizArray[questionCount].correct_answer) {
//                 element.classList.add("correct");
//             }
//         });
//     }
//
//     //clear interval(stop timer)
//     clearInterval(countdown);
//     //disable all options
//     options.forEach((element) => {
//         element.disabled = true;
//     });
// }

// Checker Function to check if option is correct or not
function checker(userOption) {
    let userSolution = userOption.innerText;
    let question =
        document.getElementsByClassName("container-mid")[questionCount];
    let options = question.querySelectorAll(".option-div");

    userOption.classList.add('selected');

    // If user clicked answer == correct option stored in object
    if (userSolution === quizArray[questionCount].correct_answer) {
        // userOption.classList.add("correct");
        scoreCount++;
    }

    // Clear interval (stop timer)
    clearInterval(countdown);
    // Disable all options
    options.forEach((element) => {
        element.disabled = true;
    });
}


//initial setup
function initial() {
    quizContainer.innerHTML = "";
    questionCount = 0;
    scoreCount = 0;
    count = 11;
    clearInterval(countdown);
    timerDisplay();
    quizCreator();
    quizDisplay(questionCount);
}

//when user click on start button
startButton.addEventListener("click", () => {
    startScreen.classList.add("hide");
    displayContainer.classList.remove("hide");
    initial();
});

//hide quiz and display start screen
window.onload = () => {
    startScreen.classList.remove("hide");
    displayContainer.classList.add("hide");
};