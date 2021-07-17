import React, {useEffect, useRef, useState} from 'react';
import './styles.css';

//const axios = require('axios');



const Search = ( props ) => {

    
    const { history } = props;
    
    console.log("================================== Search ======================================");


    const handleSearchEnter = () => {
        console.info('You clicked the Search Chip.');
        
      };
    

    const [searchText, setSearchText] = useState('Q1470929');

    const myChangeHandler = (event) => {
      setSearchText(event.target.value)
      console.log(searchText)    
  }
      

    return (
      

        <div className ="Search">

        <div className="Search-Box">
        <input className="Search-Input" type="text" name='search' onChange={myChangeHandler}/>
        

        <button className="Function-button" onClick={handleSearchEnter}>Search</button>
        </div>
        
      </div>

    );
};

export default ( Search );