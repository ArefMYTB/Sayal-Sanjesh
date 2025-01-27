import Card from "components/card";
import { MdAdd, MdDelete } from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import { TagObject } from "views/counters";
import TagForm from "components/forms/TagForm";
import { useState } from "react";

type TagsTableData = Array<{
  tagName: string;
  tagCreateDate: string;
  tagActions: JSX.Element;
}>;
const TagsTable = () => {
  const [tagName, setTagName] = useState<string>(null);
  const {
    data: tagsData,
    isLoading: tagsIsLoading,
    status: tagsStatus,
    refetch: tagsRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterTags/admin/getAll", {
        page: 1,
        count: 10,
        water_meter_tag_name: "",
        water_meter_type_create_date: "",
      }),
    queryKey: ["tagsList"],
  });

  const {
    isOpen: isTagsOpen,
    onOpen: onTagsOpen,
    onClose: onTagsClose,
  } = useDisclosure();
  const editProjectClick = (id: string) => {
    // //console.log(id);
    // onTagsOpen();
  };
  const renderTagActions = (adminId: string) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => editProjectClick(adminId)}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
        />
      </div>
    );
  };
  const tagsTableHeader = [
    { title: "نام دسته", headerKey: "tagName" },
    { title: "تاریخ ایجاد", headerKey: "tagCreateDate" },
    { title: "عملیات", headerKey: "tagActions" },
  ];
  const tableData = () => {
    let tagsTableData: TagsTableData = [];
    if (!tagsIsLoading && tagsStatus !== "pending") {
      tagsData.data.forEach((obj: TagObject) =>
        tagsTableData.push({
          tagName: obj.water_meter_tag_name,
          tagCreateDate: toPersianDate(obj.water_meter_tag_create_date),
          tagActions: renderTagActions(obj.water_meter_tag_id),
        })
      );
    }
    return tagsTableData;
  };
  return (
    <div className=" users-table-container">
      <CustomModal
        isOpen={isTagsOpen}
        onClose={onTagsClose}
        title={"دسته"}
        modalType="form"
        information={null}
        modalForm={
          <TagForm
            tagName={tagName}
            setTagName={setTagName}
            onClose={onTagsClose}
            updateTable={tagsRefetch}
          />
        }
      />
      <Card extra="border-none h-max">
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`دسته ها (${
              tagsIsLoading ? "loading..." : tagsData?.data.length
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            <CustomButton
              text="ایجاد دسته"
              onClick={onTagsOpen}
              icon={<MdAdd />}
              color="green"
              extra="ml-4"
            />
          </div>
        </div>
        <SimpleTable
          header={tagsTableHeader}
          data={tableData()}
          hasIndex={true}
          extra="!h-[65vh]"
        />
      </Card>
      <div className="pagination my-4 py-4"></div>
    </div>
  );
};
export default TagsTable;
