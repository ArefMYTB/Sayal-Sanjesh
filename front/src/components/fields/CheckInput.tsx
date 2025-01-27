import { Checkbox } from "@chakra-ui/react";
export type checkInputData = {
  id: string;
  name: string;
};
interface CheckInputProps {
  checkTitle?: string;
  inputsData: checkInputData[];
  checkedData: string[];
  setCheckedData: React.Dispatch<string[]>;
}
const CheckInput = (props: CheckInputProps) => {
  const { checkTitle, inputsData, checkedData, setCheckedData } = props;
  const checkClicked = (id: string) => {
    let selected = [...checkedData];
    selected.includes(id)
      ? setCheckedData(selected.filter((d) => d !== id))
      : setCheckedData([...selected, id]);
  };
  return (
    <>
      {checkTitle ? (
        <label
          className={`ml-3 text-sm font-bold  text-navy-700 dark:text-white`}
        >
          {checkTitle}
        </label>
      ) : (
        <></>
      )}
      <div className=" grid grid-cols-2 gap-4 ">
        {inputsData.map((input) => (
          <Checkbox
            key={input.id}
            isChecked={checkedData.includes(input.id)}
            onChange={(e) => checkClicked(input.id)}
          >
            {input.name}
          </Checkbox>
        ))}
      </div>
    </>
  );
};
export default CheckInput;
