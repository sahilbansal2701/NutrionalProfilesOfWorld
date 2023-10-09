import './App.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import 'bootstrap/dist/css/bootstrap.min.css';
import CountryData from './nutrition_profile_clusters.json'
import React, {useState, useEffect, useRef} from "react";
// import OtherCountryList from './ListGroup';
import Modal from 'react-bootstrap/Modal';


function App() {

  // false if human, true if computer
  const [country, setCountry] = useState("");
  const [year, setYear] = useState("");
  const [otherCountry, setOtherCountry] = useState("");
  const [protein, setProtein] = useState("");
  const [fat, setFat] = useState("");
  const [carbs, setCarbs] = useState("");
  const [countryFound, setCountryFound] = useState(false)

  const [show, setShow] = useState(false);
  const [show2, setShow2] = useState(false);
  const isMounted = useRef(0);


  //YEAR MODAL
  const handleClose = () => {setShow(false)};
  const handleShow = () => { 
    if (year < 2000 || year > 2013){
      setShow(true)
      setOtherCountry("")
      setCarbs("")
      setProtein("")
      setFat("")
    }
        
  };

  //COUNTRY MODAL
  const handleClose2 = () => {setShow2(false)};
  const handleShow2 = () => { 
    if (countryFound === false){
      setShow2(true)
      setOtherCountry("")
      setCarbs("")
      setProtein("")
      setFat("")
    }
        
  };

  const setCountryName = (event) => {
    console.log("target value:", event.target.value)
    setCountry(event.target.value);
  }

  const setYearInput = (event) => {
    console.log("target value:", event.target.value)
    setYear(event.target.value);
  }


  const parseJSON = () => {
    // let dataObj = JSON.parse(CountryData)
    console.log("HERE")
      for(let key in CountryData){
        // console.log("key", typeof(key))
        // console.log("year type", typeof(year))
        if(key === year) {
          console.log("key and year are equal", key, year)
          // console.log("other country:", CountryData[key])
          for (let key2 in CountryData[key]){
            // console.log("key2:", key2)
            if(key2 === country.toLowerCase()){

              setCountryFound(true)
              

              console.log("country and key2 are equal", CountryData[key][key2])
              let country_list = CountryData[key][key2]["other_countries"]
              country_list = Object.values(country_list);
              console.log("country list", country_list)
              country_list = country_list.map((number) =><li>{number}</li>);
              setOtherCountry(country_list)

              let fat_p = CountryData[key][key2]["fat_p"]
              fat_p = fat_p.toFixed(2)
              fat_p = fat_p.toString() + "%"
              setFat(fat_p)

              let protein_p = CountryData[key][key2]["protein_p"]
              protein_p = protein_p.toFixed(2)
              protein_p = protein_p.toString() + "%"
              setProtein(protein_p)

              let carb_p = CountryData[key][key2]["carbohydrates_p"]
              carb_p = carb_p.toFixed(2)
              carb_p = carb_p.toString() + "%"
              setCarbs(carb_p)
              console.log("country Found", countryFound)
              break
            }

            setCountryFound(false);
          } 
        }
      }
  }
  const formSubmit = async (e) => { 
    e.preventDefault()
    console.log("year", year)
    console.log("country", country)
    parseJSON()
    console.log("other countries:", otherCountry)
    console.log("fat:", fat)
    console.log("protein:", protein)
    console.log("carbs", carbs)
    console.log("country Found2", countryFound)
    handleShow();
    // if (isMounted.current === 1) {
    //   console.log("MOUNTED2", isMounted.current)
    //   handleShow2();
    //   isMounted.current += 1;
    // }

  }
  
  useEffect(() => {
    // parseJSON();
    // console.log("other countries:", otherCountry)
    // console.log("fat:", fat)
    // console.log("protein:", protein)
    // console.log("carbs", carbs)
    console.log("RENDER 1")
    console.log("MOUNTED", isMounted.current)
    if (isMounted.current >= 1) {
      console.log("MOUNTED2", isMounted.current)
      console.log("COUNTRY FOUND2", countryFound)
      handleShow2();
      setCountryFound(true)
      isMounted.current += 1;
    } else {
      isMounted.current += 1;
    }
    
    console.log("MOUNTED", isMounted.current)
    
  
  },[countryFound])

  return (
    <div className="App">
      <h1>Nutritional Profiles of Countries Around the World</h1>
      <p className='subtitle'>ʕ •ᴥ• ʔʕ •ᴥ• ʔ The Nourishing Four ʕ •ᴥ• ʔʕ •ᴥ• ʔ </p>
      <div className="parentDiv">
        <div className="child">
          <p className="headers"><b>TYPE IN A COUNTRY AND YEAR</b></p>
            <Form onSubmit={formSubmit} > 
              <Form.Group className="mb-3" controlId="country">
                <Form.Label>Country Name</Form.Label>
                <Form.Control type="country" placeholder="Enter a country name" onChange={setCountryName} value={country}/>
              </Form.Group>

              <Form.Group className="mb-3" controlId="year">
                <Form.Label>Year</Form.Label>
                <Form.Control type="year" placeholder="Enter a year from 2000-2013" onChange={setYearInput} value={year}/>
              </Form.Group>
              <Button variant="outline-light" type="submit">
                Submit
              </Button>
            </Form>

        </div>
        <div className="child">
          <p className="headers"><b>RESULTS:</b></p>
          <div className='results'>
            <div className='other_countries'>
              <p><b>Other countries with similar nutritional profiles:</b> 
                  <div className='listGroup'>
                    {otherCountry} 
                  </div>
              </p>
            </div>

            <div className='fat_p'>
              <p><b>The percentage of fat in a persons diet:</b> {fat}</p>
            </div>
            <div className='protein_p'>
              <p><b>The percentage of protein in a persons diet:</b> {protein}</p>
            </div>
            <div className='carbohydrate_p'>
              <p><b>The percentage of carbohydrates in a persons diet:</b> {carbs}</p>
            </div>
          </div>
          
        </div>

      </div>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Invalid Year Error</Modal.Title>
        </Modal.Header>
        <Modal.Body>Input Year is not between 2000 and 2013</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal show={show2} onHide={handleClose2}>
        <Modal.Header closeButton>
          <Modal.Title>Invalid Country Error</Modal.Title>
        </Modal.Header>
        <Modal.Body>Input country cannot be found.</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose2}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default App;
