import { Navbar } from "@/components/Navbar";


export default function InLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
      <section>
        <Navbar />
        {children}
      </section>
  );
}
