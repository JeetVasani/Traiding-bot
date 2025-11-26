export default function ResponseBox({ response }: any) {
  return (
    <pre className="bg-black text-green-400 p-4 rounded text-sm overflow-x-auto mt-4">
      {response}
    </pre>
  );
}
