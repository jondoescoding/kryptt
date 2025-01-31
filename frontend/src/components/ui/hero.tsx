"use client";

import { MoveRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";
import { IconBuildingBank, IconRobot, IconChartBar, IconCreditCard } from "@tabler/icons-react";

export function Hero() {
  const features = [
    {
      title: "Alpaca Integration",
      description: "Seamless signup and KYC process with Alpaca's Jamaican-friendly infrastructure for global market access.",
      icon: <IconBuildingBank className="w-6 h-6" />,
    },
    {
      title: "Natural Language Trading",
      description: "Trade effortlessly using simple commands like 'Buy $50 AAPL' - no technical expertise needed.",
      icon: <IconRobot className="w-6 h-6" />,
    },
    {
      title: "Portfolio Dashboard",
      description: "Track your Alpaca account balance and view your complete transaction history at a glance.",
      icon: <IconChartBar className="w-6 h-6" />,
    },
    {
      title: "Easy Donations",
      description: "Support the platform through our integrated Paddle donation system, completely separate from trading funds.",
      icon: <IconCreditCard className="w-6 h-6" />,
    },
  ];

  return (
    <>
      <div className="relative bg-black pt-24 pb-16 lg:pt-32 lg:pb-24">
        {/* Background gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-black to-black/90" />
        
        <div className="container relative mx-auto px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            {/* Left Column - Content */}
            <div className="flex flex-col space-y-8">
              {/* Main headline */}
              <h1 className="font-bold text-4xl sm:text-5xl lg:text-6xl tracking-tight text-white">
                <span className="text-yellow-400">Finally</span>, a trading app that{" "}
                <span className="text-yellow-400">just works</span>.
              </h1>

              {/* Subheadline */}
              <h2 className="font-medium text-xl sm:text-2xl lg:text-3xl text-white/80 max-w-xl">
                Simplify your access to global markets without the confusion.
              </h2>

              {/* Body text */}
              <p className="font-normal text-lg text-white/70 max-w-xl leading-relaxed">
                Most trading apps are a confusing mess of charts and jargon that leave you feeling lost.
                <br /><br />
                We&apos;ve stripped away the complexity and built something different—
                <span className="font-medium text-yellow-400">something Jamaicans actually need</span>.
              </p>

              {/* CTA buttons */}
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Button 
                  size="lg" 
                  className="bg-yellow-400 hover:bg-yellow-500 text-black font-medium text-lg px-8 py-6 h-auto transition-all"
                  asChild
                >
                  <Link href="/dashboard">
                    Get Started Now <MoveRight className="w-5 h-5 ml-2" />
                  </Link>
                </Button>
                <Button 
                  size="lg" 
                  variant="outline" 
                  className="border-white/20 hover:bg-white/10 text-white font-medium text-lg px-8 py-6 h-auto transition-all"
                  asChild
                >
                  <Link href="/contact">
                    Learn More
                  </Link>
                </Button>
              </div>
            </div>

            {/* Right Column - Image */}
            <div className="relative aspect-[4/3] rounded-xl overflow-hidden">
              <Image
                src="/images/hero/trading-interface-showcase.jpg"
                alt="Trading interface showcase"
                fill
                className="object-cover"
                priority
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-black">
        <div className="container mx-auto px-4">
          {/* Features Title */}
          <div className="mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold tracking-tight mb-4 text-white">Why Choose Kryptt?</h2>
            <p className="text-lg font-normal text-white/70 max-w-2xl leading-relaxed">Experience the future of trading with features designed specifically for Jamaican investors.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 pb-16">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="group relative p-8 border border-white/10 rounded-lg hover:border-yellow-400/50 transition-all duration-300"
              >
                <div className="mb-6 text-yellow-400">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-medium mb-3 text-white group-hover:text-yellow-400 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-base font-normal text-white/70 leading-relaxed">
                  {feature.description}
                </p>
                <div className="absolute left-0 top-0 h-full w-1 bg-yellow-400/0 group-hover:bg-yellow-400 transition-all duration-300 rounded-tl-lg rounded-bl-lg" />
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
} 