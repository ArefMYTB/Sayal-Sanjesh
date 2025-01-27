import CustomButton from "components/button";
import DateInput from "components/fields/DateInput";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";

interface ComparisonFilterProps {
  fromDate?: any;
  setFromDate?: React.Dispatch<any>;
  tillDate?: any;
  setTillDate?: React.Dispatch<any>;
  tagSelect: DynamicOption[] | null;
  tag: DynamicOption | null;
  setTag: React.Dispatch<any>;
  projectSelect: DynamicOption[] | null;
  project: DynamicOption | null;
  setProject: React.Dispatch<any>;
  counter?: DynamicOption | null;
  setCounter?: React.Dispatch<any>;
  counterSelect?: DynamicOption[] | null;
  otherCountersSelect?: DynamicOption[] | null;
  otherCounters?: DynamicOption[];
  setOtherCounters: React.Dispatch<any>;
  compaire?: Function;
  // restart?: Function;
}
const ComparisonFilter = (props: ComparisonFilterProps) => {
  const {
    tagSelect,
    tag,
    setTag,
    projectSelect,
    project,
    setProject,
    fromDate,
    setFromDate,
    tillDate,
    setTillDate,
    counterSelect,
    counter,
    setCounter,
    otherCountersSelect,
    otherCounters,
    setOtherCounters,
    compaire,
    // restart,
  } = props;
  // format("jYYYY/jM/jD")
  // format("YYYY-M-D")
  //   //console.log(otherCounters);
  return (
    <>
      <div
        className={`grid grid-cols-1 gap-4 py-4 md:grid-cols-4  xl:grid-cols-6`}
      >
        <DateInput label="تاریخ شروع" value={fromDate} onChange={setFromDate} />
        <DateInput
          label="تاریخ پایان"
          value={tillDate}
          onChange={setTillDate}
        />
        <SelectInput
          label="دسته بندی"
          placeholder="دسته بندی را انتخاب کنید"
          dynamicOptions={tagSelect}
          state={tag}
          setState={setTag}
          isMandatory={true}
          disabled={counter ? true : false}
        />
        <SelectInput
          label="پروژه "
          placeholder="پروژه  را انتخاب کنید"
          dynamicOptions={projectSelect}
          state={project}
          setState={setProject}
          disabled={counter ? true : false}
        />

        <div className="col-span-1  md:col-span-2">
          <SelectInput
            label="کنتور معیار"
            placeholder="معیار را انتخاب کنید"
            dynamicOptions={counterSelect}
            state={counter}
            setState={setCounter}
            disabled={project && otherCounters.length === 0 ? false : true}
          />
        </div>
        <div className=" col-span-1 md:col-span-2 xl:col-span-5">
          <SelectInput
            label="کنتورهای دیگر"
            placeholder="کنتورهای دیگر را انتخاب کنید"
            dynamicOptions={otherCountersSelect}
            state={otherCounters}
            setState={setOtherCounters}
            isMulti={true}
            extra="lg:col-span-5"
            disabled={counter ? false : true}
          />
        </div>
        {/* <CustomButton
          text="پاک کردن"
          color="orange"
          onClick={() => restart()}
          extra=" h-[50px]  self-end w-max !ml-0"
          // isDisabled={otherCounters.length === 0 ? true : false}
        /> */}
        <CustomButton
          text="مقایسه مصرف"
          color="red"
          onClick={() => compaire()}
          extra=" h-[50px]  self-end w-max !ml-0"
          isDisabled={otherCounters.length === 0 ? true : false}
        />
      </div>
    </>
  );
};
export default ComparisonFilter;
