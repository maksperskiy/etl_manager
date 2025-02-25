import { DataSource, RendererProps } from "../types";

export default function DateRenderer(props: RendererProps) {
  const convert = (dateString: string | number) =>
    ((date: Date, pad: (value: number) => string) =>
      `${pad(date.getDate())}.${pad(date.getMonth())}.${date.getFullYear()} ${pad(date.getHours())}:${pad(date.getMinutes())}`
    )(
      new Date(dateString),
      (value: number) => value.toString().padStart(2, '0')
    );

  return <>{ props.dataSource[props.key as keyof DataSource] && convert(props.dataSource[props.key as keyof DataSource]) }</>;
}
