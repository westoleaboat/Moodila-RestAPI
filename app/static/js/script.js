console.log('hi!')

const tabs = Array.from(document.querySelectorAll("[data-tabs]"))
const socket = io.connect('http://127.0.0.1:5000');

// Get the modal element
const modal = document.querySelector(".modal");

// Get all "Read more" buttons
const readMoreButtons = document.querySelectorAll(".read-more-btn");

// Get the <span> element that closes the modal
const closeBtn = document.querySelector(".close");

// Get the <p> element inside the modal that displays the full quote
const fullQuoteContent = document.getElementById("full-quote-content");

let selectedQuote;

// main tab
tabs.forEach((tab, index) => {

    tab.addEventListener("click", () => {
  
      // index number of selected tab
      const indexnum = Array.from(tabs).indexOf(tab);
      console.log('indexnum of selected tab: ' + indexnum)
      // Get the id of the clicked tab and log it to the console
      const selectedTabId = tabs[index].id;
      console.log('this is ID: ' +selectedTabId);
      // const selectedQuote = tabs[index].innerHTML;
      const quoteElement = tab.querySelector('.single-mood-quote .quote p');
      // console.log(quoteElement)
      selectedQuote = quoteElement.textContent.trim();

      console.log('this is the Quote: '+selectedQuote)
      // title = contents[index].querySelector('h2')
      // console.log(title.value)
      
      socket.emit('selected_id', {value: selectedTabId, indexnum: indexnum});//, id: id});
      // socket.emit('selected_title', {title: selectedQuote});

  
    }) 
});


// Loop through each "Read more" button and add event listeners
readMoreButtons.forEach(button => {
  button.addEventListener("click", () => {
      // Get the full quote content from the hidden <p> element


      console.log('click!')
      console.log(modal)
      // Show the modal
      modal.style.display = "block";
      // console.log(fullQuoteContent.textContent)
  });
});

// Listen for the 'message' event
socket.on('try_message', function(try_message) {
  // Handle the received message
  console.log('Received message:', try_message);
  // You can display the message in the UI as needed
});

    
