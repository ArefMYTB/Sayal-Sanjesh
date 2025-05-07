import moment from "moment-jalaali";
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
  Text,
} from "@chakra-ui/react";

const formatJalaliDate = (dateTime: string) => {
    return moment(dateTime, "YYYY-M-D HH:mm:ss").format("jYYYY/jM/jD");
  };
  
  const formatJalaliTime = (dateTime: string) => {
    return moment(dateTime, "YYYY-M-D HH:mm:ss").format("HH:mm:ss");
  };  

const ComparisonContent = ({
  itemA,
  itemB,
  diffDays,
  diffMechanicValue,
  diffCumulativeValue,
  percentageError,
}: {
  itemA: any;
  itemB: any;
  diffDays: number;
  diffMechanicValue: number;
  diffCumulativeValue: number;
  percentageError: string;
}) => {
  return (
    <>
        <Text fontSize="xl" fontWeight="bold" mb={4} textAlign="center">
            مقایسه برداشت‌ها
        </Text>
        <div className="flex flex-col md:flex-row gap-6 items-start justify-center">

            {/* Table Section */}
            <div className="self-stretch overflow-auto border rounded-lg p-4 min-w-[400px]">
                <Table variant="simple" size="md">
                <Thead>
                    <Tr>
                        <Th fontSize="l" textAlign="center">ویژگی</Th>
                        <Th fontSize="l" textAlign="center">برداشت اول</Th>
                        <Th fontSize="l" textAlign="center">برداشت دوم</Th>
                    </Tr>
                </Thead>
                <Tbody>
                    <Tr>
                        <Td textAlign="center">تاریخ</Td>
                        <Td textAlign="center">{formatJalaliDate(itemA.create_time)}</Td>
                        <Td textAlign="center">{formatJalaliDate(itemB.create_time)}</Td>
                    </Tr>
                    <Tr>
                        <Td textAlign="center">ساعت</Td>
                        <Td textAlign="center">{formatJalaliTime(itemA.create_time)}</Td>
                        <Td textAlign="center">{formatJalaliTime(itemB.create_time)}</Td>
                    </Tr>

                    <Tr>
                        <Td textAlign="center">مقدار مکانیکی</Td>
                        <Td textAlign="center">{itemA.mechanic_value}</Td>
                        <Td textAlign="center">{itemB.mechanic_value}</Td>
                    </Tr>
                    <Tr>
                        <Td textAlign="center">مقدار تجمعی</Td>
                        <Td textAlign="center">{itemA.cumulative_value}</Td>
                        <Td textAlign="center">{itemB.cumulative_value}</Td>
                    </Tr>
                    <Tr>
                        <Td colSpan={3}>
                            <div className="border-t-2 border-black my-2"></div>
                        </Td>
                    </Tr>
                    <Tr>
                        <Td textAlign="center">تفاوت روزها</Td>
                        <Td colSpan={2} textAlign="center">
                            {diffDays} روز
                        </Td>
                    </Tr>
                    <Tr>
                        <Td textAlign="center">تفاوت مقدار مکانیکی</Td>
                        <Td colSpan={2} textAlign="center">
                            {diffMechanicValue}
                        </Td>
                    </Tr>
                    <Tr>
                        <Td textAlign="center">تفاوت مقدار تجمعی</Td>
                        <Td colSpan={2} textAlign="center">
                            {diffCumulativeValue}
                        </Td>
                    </Tr>
                    <Tr>
                        <Td textAlign="center">درصد خطا</Td>
                        <Td colSpan={2} textAlign="center">
                            {percentageError}%
                        </Td>
                    </Tr>
                </Tbody>
                </Table>
            </div>

            {/* Images Section */}
            <div className="flex flex-col gap-4 items-center">
                <div>
                <h3 className="text-center font-bold">تصویر برداشت اول</h3>
                {itemA.image && itemA.image.length > 0 ? (
                    <div className="mt-2 flex flex-wrap justify-center gap-2">
                    {itemA.image.map((imgUrl: string, idx: number) => (
                        <img
                        key={idx}
                        src={imgUrl}
                        alt={`snapshotA-${idx}`}
                        className="h-60 w-60 rounded border object-cover"
                        />
                    ))}
                    </div>
                ) : (
                    "-"
                )}
                </div>

                <div>
                <h3 className="text-center font-bold">تصویر برداشت دوم</h3>
                {itemB.image && itemB.image.length > 0 ? (
                    <div className="mt-2 flex flex-wrap justify-center gap-2">
                    {itemB.image.map((imgUrl: string, idx: number) => (
                        <img
                        key={idx}
                        src={imgUrl}
                        alt={`snapshotB-${idx}`}
                        className="h-60 w-60 rounded border object-cover"
                        />
                    ))}
                    </div>
                ) : (
                    "-"
                )}
                </div>
            </div>
        </div>
    </>
  );
};

export default ComparisonContent;
