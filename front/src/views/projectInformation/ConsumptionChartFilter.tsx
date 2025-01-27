import CustomButton from "components/button";
import DateInput from "components/fields/DateInput";
import InputField from "components/fields/InputField";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import { renderUnit } from "utils/CommonFunctions";

interface ProjectConsumptionChartFilterProps {
  tagSelect: DynamicOption[] | null;
  tag: DynamicOption | null;
  setTag: React.Dispatch<any>;
  fromDate: any;
  setFromDate: React.Dispatch<any>;
  tillDate: any;
  setTillDate: React.Dispatch<any>;
  update: any;
  total?: number | null;
  tab: "records" | "chart" | "event";
}
const ProjectConsumptionChartFilter = (
  props: ProjectConsumptionChartFilterProps
) => {
  const {
    tagSelect,
    tag,
    setTag,
    fromDate,
    setFromDate,
    tillDate,
    setTillDate,
    update,
    tab,
    total,
  } = props;
  // format("jYYYY/jM/jD")
  // format("YYYY-M-D")
  // //console.log(total);
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
              } ${renderUnit(tag.label, false)}`}
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
        />
      </div>
      <div className={`grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 `}>
        <SelectInput
          label="دسته بندی"
          placeholder="دسته بندی مورد نظر را انتخاب کنید"
          dynamicOptions={tagSelect}
          state={tag}
          setState={setTag}
          isMandatory={true}
        />
      </div>
    </>
  );
};
export default ProjectConsumptionChartFilter;
