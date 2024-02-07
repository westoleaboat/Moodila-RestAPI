console.log('hi!')

const tabs = Array.from(document.querySelectorAll("[data-tabs]"))
const socket = io.connect('http://localhost:5000');


// main tab
tabs.forEach((tab, index) => {

    tab.addEventListener("click", () => {
      //with everyclick first default all the class settings (remove all selcted classes)
    //   contents.forEach((content) => {
    //     content.classList.remove("selected")
    //   })
    //   tabs.forEach((tab) => {
    //     tab.classList.remove("selected")
    //   })
  
    //   //adding the active class for current project and tab
    //   contents[index].classList.add("selected")
    //   tabs[index].classList.add("selected")
  
  
      // index number of selected tab
      const indexnum = Array.from(tabs).indexOf(tab);
      console.log('indexnum of selected tab ' + indexnum)
  
  
      // log info of selected tab when click
      // console.log(tabs[index].innerHTML)
      // console.log(tabs[index].outerHTML)
  
      // Get the id of the clicked tab and log it to the console
      const selectedTabId = tabs[index].id;
      console.log('this is ID: ' +selectedTabId);
  
      // obtain title
      const selectedTitle = tabs[index].innerHTML;
      console.log('this is Title: '+selectedTitle)
      // title = contents[index].querySelector('h2')
      // console.log(title.value)
      
      socket.emit('selected_id', {value: selectedTabId, indexnum: indexnum});//, id: id});
      socket.emit('selected_title', {title: selectedTitle});

  
    }) });


    
    
