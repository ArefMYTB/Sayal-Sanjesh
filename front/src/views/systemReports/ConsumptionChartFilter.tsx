import CustomButton from "components/button";
import DateInput from "components/fields/DateInput";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";

interface ConsumptionChartFilterProps {
  tagSelect: DynamicOption[] | null;
  tag: DynamicOption | null;
  setTag: React.Dispatch<any>;
  userSelect: DynamicOption[] | null;
  user: DynamicOption | null;
  setUser: React.Dispatch<any>;
  projectSelect: DynamicOption[] | null;
  project: DynamicOption | null;
  setProject: React.Dispatch<any>;
  typeSelect: DynamicOption[] | null;
  type: DynamicOption | null;
  setType: React.Dispatch<any>;
  fromDate?: any;
  setFromDate?: React.Dispatch<any>;
  tillDate?: any;
  setTillDate?: React.Dispatch<any>;
  update?: any;
}
const ConsumptionChartFilter = (props: ConsumptionChartFilterProps) => {
  const {
    tagSelect,
    tag,
    setTag,
    userSelect,
    user,
    setUser,
    projectSelect,
    project,
    setProject,
    typeSelect,
    type,
    setType,
    fromDate,
    setFromDate,
    tillDate,
    setTillDate,
    update,
  } = props;
  // format("jYYYY/jM/jD")
  // format("YYYY-M-D")
  const dateValidation = () => {
    update();
  };
  return (
    <>
      {fromDate ? (
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
          </div>
          <CustomButton
            text="اعمال تاریخ"
            color="brand"
            onClick={() => dateValidation()}
          />
        </div>
      ) : (
        <></>
      )}
      <div className={`grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4 `}>
        <SelectInput
          label="دسته بندی"
          placeholder="دسته بندی مورد نظر را انتخاب کنید"
          dynamicOptions={tagSelect}
          state={tag}
          setState={setTag}
          isMandatory={true}
        />

        <SelectInput
          label="پروژه "
          placeholder="پروژه مورد نظر را انتخاب کنید"
          dynamicOptions={projectSelect}
          state={project}
          setState={setProject}
          disabled={user ? true : false}
        />
        <SelectInput
          label="نوع کنتور "
          placeholder="نوع کنتور مورد نظر را انتخاب کنید"
          dynamicOptions={typeSelect}
          state={type}
          setState={setType}
        />
        <SelectInput
          label="کاربر "
          placeholder="کاربر مورد نظر را انتخاب کنید"
          dynamicOptions={userSelect}
          state={user}
          setState={setUser}
          disabled={project ? true : false}
        />
      </div>
    </>
  );
};
export default ConsumptionChartFilter;
