import Card from "components/card";
import CustomTabs from "components/tabs";
import CreateSnapshotView from "./CreateSnapshot";
const VerificationView = () => {
  //   const tabsData = [
  //     { label: "برداشت", content: <CreateSnapshotView /> },
  //     { label: "مقایسه", content: <DeviceTypesTable /> },
  //   ];

  return (
    <div className=" ">
      <Card>
        <CreateSnapshotView />
        {/* <CustomTabs tabsData={tabsData} /> */}
      </Card>
    </div>
  );
};
export default VerificationView;
