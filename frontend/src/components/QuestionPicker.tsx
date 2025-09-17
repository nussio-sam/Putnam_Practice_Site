import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios'; 

const QAPATH = 'http://localhost:3000/qa/answer';


// Pass in QA String data from global with some form of dependency injection?
export const QAComponent: React.FC = () => {

  const [selectedQuestion, setSelectedQuestion] = useState<string>('');
  const [selectedYear, setSelectedYear] = useState<number>(0);
  const [answer, setAnswer] = useState<string>('');


  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const HandleDropdownChange = (event) => {
      // setSelectedQuestion(Element.);
    }

  useEffect(() => {
    if (selectedQuestion && selectedYear) {
      setIsLoading(true);
      fetch(`${QAPATH}/qa?year=${selectedYear}&question=${selectedQuestion}`)
      .then(response => {
          if (!response.ok) {
            throw new Error('Network failure');
          }
          return response.json();
        })
      .then(data => {
          setAnswer(data.answer);
        })
      .catch(err => {
          console.error('Fetching QA response failed: ', err);
          setAnswer('An error occured, please try again later');
        })
      .finally(() => {
          setIsLoading(false);
        });
    }
      }, [selectedYear, selectedQuestion]);

 return(
  <div>
    
  </div>
 ) 
}
