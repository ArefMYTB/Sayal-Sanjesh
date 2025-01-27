import { useCallback, useEffect, useMemo, useState } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import L, { LatLngTuple } from "leaflet";
import InputField from "components/fields/InputField";
import { MdLocationPin } from "react-icons/md";
import CustomButton from "components/button";

type DisplayPositionProps = {
  map: L.Map;
};
interface GetLocationMapProps {
  lat: null | number;
  setLat: React.Dispatch<null | number>;
  lng: null | number;
  setLng: React.Dispatch<null | number>;
  isInfo?: boolean;
  editFunction?: Function;
  deviceLoc?: { lat: number; lng: number };
}
const GetLocationMap = (props: GetLocationMapProps) => {
  const { lat, setLat, lng, setLng, isInfo, editFunction, deviceLoc } = props;
  // console.log(lat);
  const center: LatLngTuple = [lat ? lat : 35.724096, lng ? lng : 51.430389];
  const zoom = 16;
  const [map, setMap] = useState<L.Map | null>(null);
  const DisplayPosition = ({ map }: DisplayPositionProps) => {
    const [position, setPosition] = useState<L.LatLng>(map.getCenter());
    // console.log("pos : ", position);
    const onClick = useCallback(() => {
      map.setView(center, zoom);
    }, [map]);

    const onMove = useCallback(() => {
      setPosition(map.getCenter());
      setLat(map.getCenter().lat);
      setLng(map.getCenter().lng);
    }, [map]);

    useEffect(() => {
      map.on("move", onMove);
      return () => {
        map.off("move", onMove);
      };
    }, [map, onMove]);
    const newLocationClicked = () => {
      setLat(lat);
      setLng(lng);
      map.flyTo([lat, lng], 16, {
        animate: true,
        duration: 3,
      });
      setPosition(map.getCenter());
    };
    return (
      <div
        className={`grid grid-cols-1 items-end gap-2 ${
          isInfo ? "lg:grid-cols-4" : "lg:grid-cols-3"
        }`}
      >
        <InputField
          id="loca-lat"
          type="number"
          label="عرض جغرافیایی(lat)"
          placeholder="عرض جغرافیایی"
          state={lat}
          setState={setLat}
        />
        <InputField
          id="loca-lon"
          type="number"
          label="طول جغرافیایی(lng)"
          placeholder="طول جغرافیایی"
          state={lng}
          setState={setLng}
        />
        <div
          className="m-1 max-w-[80px] cursor-pointer rounded-md bg-brand-400 px-2 py-1 text-center text-white"
          onClick={() => newLocationClicked()}
        >
          اعمال
        </div>
        <CustomButton
          text="تغییر موقعیت مکانی"
          color="green"
          // isDisabled={
          //   deviceLoc.lat === lat && deviceLoc.lng === lng ? true : false
          // }
          isDisabled={true}
          onClick={() => editFunction()}
          extra="max-w-40"
        />
      </div>
    );
  };

  const displayMap = useMemo(
    () => (
      <MapContainer
        center={center}
        zoom={zoom}
        scrollWheelZoom={false}
        ref={setMap}
        zoomControl={true}
        className="my-2 h-full w-full"
      >
        <TileLayer
          // attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {/* <TileLayer
          // attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
          url="https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
          //  maxZoom= {20}
          subdomains={["mt1", "mt2", "mt3"]}
        /> */}
      </MapContainer>
    ),
    []
  );
  return (
    <div className="pick-location relative ">
      {map ? <DisplayPosition map={map} /> : null}

      <div className=" relative">
        {" "}
        <span
          className=" location-pin absolute z-[1000]
       flex h-10 w-10 items-center justify-center "
        >
          <span className="h-full w-full text-3xl text-green-600">
            <MdLocationPin />
          </span>
        </span>{" "}
        <div className=" z-50 h-96 w-full">{displayMap}</div>
      </div>
    </div>
  );
};

export default GetLocationMap;
