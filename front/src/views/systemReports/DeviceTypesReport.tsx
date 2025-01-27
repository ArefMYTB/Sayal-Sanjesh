import { useQuery } from "@tanstack/react-query";
import Loading from "components/loading";
import { useId } from "react";
import { reqFunction } from "utils/API";
import Widget from "views/rtl/default/components/Widget";

const DeviceTypesReport = () => {
  const {
    data: deviceTypeData,
    isLoading: deviceTypeIsLoading,
    status: deviceTypeStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterTypes/admin/total/statistics", {}, "get"),
    queryKey: ["deviceTypeStatistics"],
  });
  const uniqId = useId();
  return (
    <>
      {!deviceTypeIsLoading && deviceTypeStatus === "success" ? (
        <div className="projects-overview pt-4">
          <div className="pb-4 text-xl font-bold text-navy-700 dark:text-white">
            آمار کلی
          </div>
          <div className=" mt-3 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            <Widget
              title={"تعداد نوع کنتور"}
              subtitle={`${deviceTypeData.data.all_counter_types} عدد`}
            />
            <Widget
              title={"نوع کنتور با بیشترین تعداد"}
              subtitle={`${deviceTypeData.data.types_with_max_counter[0].water_meter_type_name} با ${deviceTypeData.data.types_with_max_counter[0].number_of_counter} عدد`}
            />
            {deviceTypeData.data.tags_info.map(
              (
                tag: { water_meter_tag_name: string; number_of_type: number },
                id: any
              ) => (
                <Widget
                  key={id + uniqId}
                  title={`تعداد نوع کنتور ${tag.water_meter_tag_name}`}
                  subtitle={`${tag.number_of_type} عدد`}
                />
              )
            )}
          </div>
        </div>
      ) : (
        // <div>loading or err</div>
        <Loading />
      )}
    </>
  );
};
export default DeviceTypesReport;
