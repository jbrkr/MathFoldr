import React, {useEffect, useRef, useState} from 'react';
import DataService from '../../services/DataService';

import styles from './styles';

const SummaryStats = ( props ) => {
    const {classes} = props;
    const { history } = props;

    console.log("================================== Summary Stats ======================================");

    console.log(props);


    // Component States
    
    const [stats , setStats] = useState([]);
    const [statsTable, setStatsTable] = useState([]);
    
    const loadStats = () => {
        if(stats){
            setStatsTable(stats);
        }else{
            setStatsTable(null);
        }
    }
    const [refresh , setRefresh] = useState(0);

    // State holder for reference in handlers
    let state = {
        "stats": stats,
        "refresh":refresh,
        "setRefresh":setRefresh
    }
    const colorList = ["#C0504D","#1F497D", "#9BBB59","#F79646","#4BACC6","#8064A2","#948A54","#C0504D","#1F497D", "#9BBB59","#F79646","#4BACC6","#8064A2","#948A54","#C0504D","#1F497D", "#9BBB59","#F79646","#4BACC6","#8064A2","#948A54","#C0504D","#1F497D", "#9BBB59","#F79646","#4BACC6","#8064A2","#948A54","#C0504D","#1F497D", "#9BBB59","#F79646","#4BACC6","#8064A2","#948A54"]

    // Setup Component
    useEffect(() => {
        // Set state from props

        // Keydown event listener
        window.addEventListener('keydown', (event) => handleKeyDown(event, state));

        // Cleanup Component
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
      }, []);
      
    // Component functions




    return (
        <div>
            
        </div>
    );
};

export default ( SummaryStats );