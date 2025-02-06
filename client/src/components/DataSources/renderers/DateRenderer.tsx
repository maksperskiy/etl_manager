import { DataSource, RendererProps } from "../types";

export default function DateRenderer(props: RendererProps) {
  // const [value, setValue] = useState('');

  // useEffect(() => {
  //   setValue(new Date(props.dataSource[props.key as keyof DataSource]).toTimeString());
  // }, []);

  return <>{ new Date(props.dataSource[props.key as keyof DataSource]).toTimeString() }</>;
}
