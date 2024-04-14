import { useEffect, useState } from "react";
import { CPURAM } from "../health/CPURAM";
import PieChart from "../health/PieChart";
import "./Home.css";
export const Home = () => {
  const [eventData, setEventData] = useState({});
  const [pieChartData, setPieChartData] = useState({});
  const [hostname,setHostname] = useState("Default HostName");
  const [ipaddress,setIpaddress] = useState("0.0.0.0");
  const [macAddress,setMacAddress] = useState("00:00:00:00:00:00");
  const [timeStamp,setTimeStamp] = useState(null);

  const updateEventData = (data) => {
    setEventData(data);
     console.log("data updated !!",data)
  };

  useEffect(() => {
    if (Object.keys(eventData).length === 0) {
      // eventData is empty, don't do anything
    } else {
      setHostname(eventData["hostname"])
      setIpaddress(eventData["ipaddress"])
      setMacAddress(eventData["macaddress"])
      setTimeStamp(eventData["timestamp"])
      var diskData = eventData["health"]["disk"];
      var PieChartLabels = [];
      var PieChartValues = [];

      for (const key in diskData) {
        if (diskData.hasOwnProperty(key)) {
          const device = diskData[key]["device"];
          const percent = diskData[key]["percent"];
          PieChartLabels.push(device)
          PieChartValues.push(percent)
         //  console.log(`Key: ${key}, Device: ${device}`);
        }
      }
      const pieChartData = {
        labels: PieChartLabels,
        values: PieChartValues,
      };

      setPieChartData(pieChartData);
    }
  }, [eventData]);

  return (
    <>
      <div className="container">
        <h3>
          <span>Hostname - {hostname}</span>
          <ul>
          <li>
            Ipaddress - {ipaddress}
          </li>  
          <li>
            Mac Address - {macAddress}
          </li>  
          <li>
            TimeStamp - {timeStamp}
          </li>  
          </ul>
          
        </h3>
        <br/>
        <div className="row row-cols-1 row-cols-md-2 g-4">
          <div className="col">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">CPU and RAM</h5>
                <CPURAM updateEventData={updateEventData} />
              </div>
            </div>
          </div>
          <div className="col">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Disk Usage</h5>
                <PieChart data={pieChartData} />
              </div>
            </div>
          </div>
        </div>
        <hr></hr>
      </div>
    </>
  );
};
