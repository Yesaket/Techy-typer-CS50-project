//Loading the page and initializing game 
window.onload = start;

//Setting initial time and initial score 
let duration = 60; 
let score = 0;
//Boolean to tell if game is on or not, game starts immediately so setting it initially to on 
let gameon = true;

// Using Document Object Models to link the page's data and to variables in Javascript 
const typedWord = document.querySelector('#word-input');
const displayedWord = document.querySelector('#current-word');
const WPMDisplay = document.querySelector('#wpm');
const displayTime = document.querySelector('#time');
const endgametext = document.querySelector('#text');
const highscoreDisplay = document.querySelector('#highscore');

//Initializing array for words to be typed
const words = [
  'juxtaposition',
  'xanthophyll',
  'vicissitude',
  'autochthonous',
  'logorrhea',
  'viviparous',
  'samarkand',
  'insouciance',
  'eudaemonia',
  'aardwolf',
  'baccalaureate',
  'extemporaneous',
  'cardiopulmonary',
  'glockenspiel',
  'nomenclature',
  'paraphernalia',
  'schizophrenia',
  'trichotillomania',
  'vaudevillian',
  'magnanimity',
  'sgraffito',
  'Solenichthyes',
  'trabeate',
  'dibucaine',
  'dibucaine',
  'alliteration',
  'manageableness',
  'comprehendible',
  'xanthophyceae',
  'deference',
  'defoliate',
  'degradation',
  'discrepancy',
  'exceptionable',
  'fanaticism',
  'felicitous',
  'exculpate',
  'counterfeit',
  'beguile',
  'nauseous',
  'dilate',
  'indict',
  'liquefy',
  'wednesday',
  'sherbet',
  'bologna',
  'playwright',
  'fuchsia',
  'create',
  'destroy',
  'combat',
  'fight',
  'hi',
  'bye',
  'cry',
  'love',
  'you'
];

// Creating a function to pick out random words in the array and display them on the page for the user to type
function Display(words) {
  // Performing the Durstenfeld Shuffle to randomzie the elements of the words array
  function randomize(words) {
    for (var i = words.length - 1; i > 0; i--) 
  {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = words[i];
        words[i] = words[j];
        words[j] = temp;
    }
    return words[0];
}
// Output random first word in the array
displayedWord.innerHTML = randomize(words)
}

// Start the game 
function start() 
{
  // Call on the display function to get a word form the array
  Display(words);
  // Check for the event that the user starts typing in words and performing playgame function
    typedWord.addEventListener('input', playgame);
}

// Match currentWord to wordInput
function verify() {
  if (typedWord.value === displayedWord.innerHTML) {
    endgametext.innerHTML = 'Lets gooo';
    return true;
  } else 
  {
    return false;
  }
}


// Conduct the game
function playgame() 
{
  // Check that the typed word matches the displayed word
  if (verify(words)) 
  {
    typedWord.value = '';
    Display(words);
    if (gameon=true){
      score++;
    }
    else {
      score = 0;
    }
  }
  //Let the page display the value of the score variable
WPMDisplay.innerHTML = score;
}


// Keep calling countdown every second 
setInterval(countdown, 1000);
function countdown() {
    // Display the countdown
    displayTime.innerHTML = duration;
  // Keep decrease seconds by one every second as long as time is greater than 0
    if (duration > 0) {
      // Decrease time by a second
      duration--;
    } else if (duration == 0) {
      // If time is 0 then indicate game is over 
      gameon = false;
    }
  }
  
// Check if game is still running and reset score if game is over
// Check if the game is still going or not every millisecond 
setInterval(reset, 10);
function reset() {
  if (!gameon && duration === 0) {
    score = 0;
    endgametext.innerHTML = 'Game Over';
  }
}