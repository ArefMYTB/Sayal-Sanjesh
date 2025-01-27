import { useContext } from "react";
import Select from "react-select";
import { ThemeContext } from "ThemeProvider";
import { CountOption } from "variables";
export interface DynamicOption {
  value: string | boolean | number;
  label: string;
  disabled?: boolean;
}
interface SelectInputProps {
  label?: string;
  dynamicOptions: DynamicOption[] | CountOption[];
  placeholder?: string;
  state?: null | DynamicOption | DynamicOption[];
  setState?: React.Dispatch<any>;
  disabled?: boolean | null;
  isMandatory?: boolean;
  isCount?: boolean;
  setPage?: React.Dispatch<any>;
  setCount?: React.Dispatch<any>;
  isMulti?: boolean;
  extra?: string;
}
const SelectInput = (props: SelectInputProps) => {
  const {
    dynamicOptions,
    label,
    placeholder,
    state,
    setState,
    disabled,
    isMandatory,
    isCount,
    setPage,
    setCount,
    isMulti,
    extra,
  } = props;
  const { isDark } = useContext(ThemeContext);

  return (
    <div className={` mx-2 ${extra}`}>
      <label
        // htmlFor={id}
        className={` ml-3 text-sm font-bold text-navy-700 dark:text-white`}
      >
        {label}
      </label>
      <Select
        className={`${isCount ? "basic-single count-select" : "basic-single"} ${
          isDark ? "!text-white" : ""
        }`}
        classNamePrefix="select"
        defaultValue={state}
        onChange={
          isCount
            ? (event: DynamicOption | any) => {
                setPage(1);
                setCount(event);
              }
            : setState
        }
        placeholder={placeholder}
        isOptionDisabled={(option) => option.disabled}
        isDisabled={disabled ?? false}
        isLoading={false}
        isClearable={isMandatory ? false : true}
        isRtl={true}
        menuPlacement="auto"
        noOptionsMessage={({ inputValue: string }) => "انتخاب موجود نیست"}
        isSearchable={true}
        name="select"
        isMulti={isMulti ? true : false}
        options={dynamicOptions}
      />
    </div>
  );
};
export default SelectInput;
