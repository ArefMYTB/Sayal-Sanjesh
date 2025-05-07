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
      <TableContainer>
        <Table variant="simple" size="md">
          <Thead>
            <Tr>
              <Th textAlign="center">ویژگی</Th>
              <Th textAlign="center">برداشت اول</Th>
              <Th textAlign="center">برداشت دوم</Th>
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
      </TableContainer>
    </>
  );
};

export default ComparisonContent;
