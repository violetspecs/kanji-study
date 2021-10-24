const value = JSON.parse(document.getElementById('kanji-data').textContent);
const forConvert = "\"" + value.substring(1, value.length - 1) + "\"";
const quizType = document.getElementById('quizType').textContent

const kanjiList = JSON.parse(value);
let correctAnswers = [];
let wrongAnswers = [];

// Step 1: Randomize kanji list for display in quiz
let kanjiListForQuiz = shuffleArray(kanjiList.map(x => x));

console.log(kanjiListForQuiz);
let currentIndex = 0;
let score = 0;
// Step 2: Get choices for display
let choices = getChoices(currentIndex);

console.log(choices);

// Step 3: Update kanji, choices, and current item being answered for display
updateDisplay(choices);

function getChoices(index) {
    let kanji = kanjiListForQuiz[index];
    let kanjiListForProcess = kanjiListForQuiz.map(x => x);
    let answers = [];
    answers.push(kanji);

    kanjiListForProcess.splice(index, 1);

    for (var i = 0; i < 3; i++) {
        let randomIndex = Math.floor(Math.random()*kanjiListForProcess.length);
        answers.push(kanjiListForProcess[randomIndex]);
        kanjiListForProcess.splice(randomIndex, 1);
    }
    return shuffleArray(answers);
}

function getQuestion(selectedAnswer) {
    console.log("get next question");
    kanjianswer = kanjiList.filter(kanji => {
        if (kanji.id == selectedAnswer) {
            return kanji;
        }
    });
    console.log(kanjianswer);

    // Check if answer was correct and add score if correct, and add to correct answers list
    if (kanjianswer[0].id == kanjiListForQuiz[currentIndex].id) {
        score += 1;
        correctAnswers.push(kanjiListForQuiz[currentIndex].id);
    // Add to wrong answers list if wrong
    } else {
        wrongAnswers.push(kanjiListForQuiz[currentIndex].id);
    }

    if (currentIndex == kanjiList.length - 1) {
        console.log("No more questions");
        // Send form to server
        document.getElementById('correctAnswers').value = correctAnswers.join(' ');
        document.getElementById('wrongAnswers').value = wrongAnswers.join(' ');
        document.getElementById('quizChoiceType').value = quizType;
        document.getElementById("answersToSend").submit();
        return;
    }

    currentIndex += 1;
    let choices = getChoices(currentIndex);

    updateDisplay(choices);
}

function updateDisplay (choices) {
    document.getElementById('kanji').innerText = kanjiListForQuiz[currentIndex].kanji;
    for (var i = 0; i < 4; i++) {
        let choice = choices[i].english
        if (quizType == 'kunyomi') {
            choice = choices[i].kunyomi
        }
        document.getElementById('option' + (i + 1)).innerText = choice;
        document.getElementById('option' + (i + 1)).value = choices[i].id;
    }
    document.getElementById('count').innerText = (currentIndex + 1) + " out of " + kanjiListForQuiz.length;
    document.getElementById('score').innerText = "Score: " + (score) + "/" + kanjiListForQuiz.length;
}

// from stackoverflow 
function shuffleArray(array) {
    var currentIndex = array.length,  randomIndex;

    // While there remain elements to shuffle...
    while (currentIndex != 0) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;

        // And swap it with the current element.
        [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }

    return array;
}
