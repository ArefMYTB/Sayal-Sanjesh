// import Checkbox from "components/checkbox";
import { Checkbox } from "@chakra-ui/react";
import NoData from "components/noData";
import { useId } from "react";

export type HeaderObject = {
  title: string;
  headerKey: string;
};
interface SimpleTableProps {
  header: HeaderObject[];
  data: any[];
  hasIndex?: boolean;
  page?: number;
  count?: number;
  isCheckTable?: boolean;
  selectedItems?: any[];
  setSelectedItems?: React.Dispatch<any[]>;
  extra?: string;
}
const SimpleTable = (props: SimpleTableProps) => {
  const {
    header: tableHeader,
    hasIndex,
    page,
    count,
    data: tableData,
    isCheckTable,
    selectedItems,
    setSelectedItems,
    extra,
  } = props;
  const uniqId = useId();
  const allChecked = selectedItems
    ? selectedItems.length === tableData.length && selectedItems.length !== 0
      ? true
      : false
    : false;

  const isIndeterminate = selectedItems
    ? selectedItems.length > 0 && !allChecked
    : false;
  const selectAllClicked = () => {
    let all: string[] = [];
    tableData.forEach((rowObject: any) => all.push(rowObject.counterSerial));
    allChecked ? setSelectedItems([]) : setSelectedItems(all);
  };
  const rowIsChecked = (rowObject: any) => {
    return selectedItems.includes(rowObject.counterSerial);
  };
  const rowClicked = (rowObject: any) => {
    let selected: string[] = [...selectedItems];
    selected.includes(rowObject.counterSerial)
      ? setSelectedItems(
          selected.filter((item: string) => item !== rowObject.counterSerial)
        )
      : setSelectedItems([...selected, rowObject.counterSerial]);
  };
  return (
    <div className={`mt-8 ${extra} overflow-x-scroll px-4 pb-4 `}>
      {tableData.length > 0 ? (
        <table className="relative w-full border-separate">
          <thead className="bg-white dark:!bg-navy-900">
            <tr className="sticky top-0 !z-[1000]">
              {isCheckTable ? (
                <th className=" sticky top-0 border-b-[1px] border-gray-200 bg-white pb-2 pr-2 pt-4 text-center dark:!bg-navy-700">
                  <Checkbox
                    isChecked={allChecked}
                    isIndeterminate={isIndeterminate}
                    onChange={(e) => selectAllClicked()}
                  />
                </th>
              ) : null}
              {hasIndex ? (
                <th className=" sticky top-0 border-b-[1px] border-gray-200 bg-white pb-2 pr-2 pt-4 text-center dark:!bg-navy-700">
                  #
                </th>
              ) : null}
              {tableHeader.map((item, id) => (
                <th
                  key={`${id}-${uniqId}-${id}`}
                  className=" sticky top-0 border-b-[1px] border-gray-200 bg-white pb-2 pr-2 pt-4 text-center dark:!bg-navy-700"
                >
                  {item.title}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableData.map((data, idx) => (
              <tr
                key={`${uniqId}-${idx}`}
                className="hover:bg-gray-50 dark:hover:bg-navy-700"
              >
                {isCheckTable ? (
                  <td className=" w-10border-white/0 mx-auto  py-3 pr-2 text-center">
                    <Checkbox
                      isChecked={rowIsChecked(data)}
                      onChange={(e) => rowClicked(data)}
                    />
                  </td>
                ) : null}
                {hasIndex ? (
                  <td className=" w-10border-white/0 mx-auto  py-3 pr-2 text-center">
                    {page && count ? (page - 1) * count + idx + 1 : idx + 1}
                  </td>
                ) : null}
                {tableHeader.map((d, i) => (
                  <td
                    className="mx-auto min-w-[150px] border-white/0  py-3 pr-4 text-center"
                    key={`${i}-${uniqId}`}
                  >
                    {data[d.headerKey]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <NoData />
      )}
    </div>
  );
};
export default SimpleTable;
