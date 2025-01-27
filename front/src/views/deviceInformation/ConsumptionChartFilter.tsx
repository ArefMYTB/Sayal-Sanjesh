import CustomButton from "components/button";
import DateInput from "components/fields/DateInput";
import InputField from "components/fields/InputField";
import { DynamicOption } from "components/fields/SelectInput";
import { renderUnit } from "utils/CommonFunctions";

interface ProjectConsumptionChartFilterProps {
  fromDate: any;
  setFromDate: React.Dispatch<any>;
  tillDate: any;
  setTillDate: React.Dispatch<any>;
  update: any;
  chartTag: DynamicOption;
  total?: number | null;
  tab: "records" | "chart" | "event";
}
const ProjectConsumptionChartFilter = (
  props: ProjectConsumptionChartFilterProps
) => {
  const {
    fromDate,
    setFromDate,
    tillDate,
    setTillDate,
    update,
    chartTag,
    total,
    tab,
  } = props;
  const dateValidation = () => {
    update();
  };
  return (
    <>
      <div className=" flex flex-col items-end justify-between md:flex-row">
        <div
          className={`grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 `}
        >
          <DateInput
            label="تاریخ شروع"
            value={fromDate}
            onChange={setFromDate}
          />
          <DateInput
            label="تاریخ پایان"
            value={tillDate}
            onChange={setTillDate}
          />
          {tab === "chart" ? (
            <InputField
              label="مصرف کل"
              state={`${
                total !== 0 && total
                  ? Math.round(total).toLocaleString()
                  : "صفر"
              } ${renderUnit(chartTag.label, false)}`}
              id={"total-consumption"}
              disabled={true}
              placeholder={"مصرف کل در بازه انتخابی"}
            />
          ) : null}
        </div>
        <CustomButton
          text="اعمال تاریخ"
          color="brand"
          onClick={() => dateValidation()}
          extra="min-w-[98px] "
        />
      </div>
    </>
  );
};
export default ProjectConsumptionChartFilter;
