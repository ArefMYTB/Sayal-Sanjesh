import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import { Icon, LatLngTuple } from "leaflet";
import RedPin from "../../../src/assets/img/avatars/redPin.png";
import BluePin from "../../../src/assets/img/avatars/bluePin.png";
// import Pin from "../../../src/assets/img/avatars/location marker_5990782.png";
// import "./styles.css";
import "leaflet/dist/leaflet.css";
import { useContext } from "react";
import { ThemeContext } from "ThemeProvider";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import Loading from "components/loading";
import { Link } from "react-router-dom";
export type counterLocationsInfo = {
  water_meter_location: {
    lat: number | string;
    lng: number | string;
  };
  water_meter_serial: string;
  water_meter_name: string;
  water_meter_project__water_meter_project_name: string;
  water_meter_type__water_meter_tag__water_meter_tag_name: string;
  water_meter_type__water_meter_type_name: string;
};
const CustomMap = () => {
  const { isDark } = useContext(ThemeContext);
  const customPowerIcon = new Icon({
    iconUrl: RedPin,
    iconSize: [30, 30], // adjust size px
  });
  const customWaterIcon = new Icon({
    iconUrl: BluePin,
    iconSize: [30, 30], // adjust size px
  });
  let center: LatLngTuple = [32.10894904606479, 53.493205120165686];
  //get counter locations
  const {
    data: countersLocation,
    isLoading: locationsLoading,
    status: locationsStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction(
        "watermeters/admin/getlocations",
        {
          type_id_list: null,
          project_id_list: null,
          tag_id_list: null,
        },
        "post"
      ),
    queryKey: ["counterslocation"],
  });
  const renderPins = (locationsList: counterLocationsInfo[]) => {
    let validLocations = locationsList.filter(
      (location) =>
        typeof location.water_meter_location !== "string" &&
        Number(location.water_meter_location.lat)
    );

    return (
      <>
        {validLocations.map((loc, idx) => (
          <Marker
            position={[
              Number(loc.water_meter_location.lat),
              Number(loc.water_meter_location.lng),
            ]}
            icon={
              loc.water_meter_type__water_meter_tag__water_meter_tag_name ===
              "آب"
                ? customWaterIcon
                : customPowerIcon
            }
            key={idx + loc.water_meter_serial + idx}
          >
            <Popup>
              <span className="text-center !font-dm font-bold">
                {loc.water_meter_name}
              </span>
              <br />
              <Link
                to={`/admin/counters/${loc.water_meter_serial}`}
                rel="noopener noreferrer"
              >
                <span className=" text-center !font-dm text-blue-600 dark:text-red-600">
                  مشاهده جزئیات
                </span>
              </Link>
            </Popup>
          </Marker>
        ))}
      </>
    );
  };
  return (
    <div className={isDark ? "dark" : ""}>
      {!locationsLoading && locationsStatus === "success" ? (
        <MapContainer
          center={center}
          zoom={5}
          style={{
            height: "70vh",
            width: "100%",
            padding: "10px",
            margin: "0 auto",
          }}
        >
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {/* <TileLayer
            // attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
            url="https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
            //  maxZoom= {20}
            subdomains={["mt1", "mt2", "mt3"]}
          /> */}
          {renderPins(countersLocation?.data)}
        </MapContainer>
      ) : (
        <Loading />
      )}
    </div>
  );
};
export default CustomMap;
