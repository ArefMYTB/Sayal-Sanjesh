import Card from "components/card";
import CustomTabs from "components/tabs";
import DeviceTypesTable from "./DeviceTypesTable";
import CreateSnapshotView from "./CreateSnapshot";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
const VerificationView = () => {
    

    return (
        <div className=" ">
        <Card>
            <CreateSnapshotView/>
        </Card>
        </div>
    );
};
export default VerificationView;
