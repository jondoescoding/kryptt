"use client";

import { useEffect, useRef, useState } from "react";
import * as Plot from "@observablehq/plot";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RefreshCw, AlertCircle } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";

// Types for our account data
interface AccountData {
  equity: string;
  cash: string;
  buying_power: string;
  long_market_value: string;
  short_market_value: string;
  daytrade_count: number;
  pattern_day_trader: boolean;
}

export default function DashboardPage() {
  const [accountData, setAccountData] = useState<AccountData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const chartRef = useRef<HTMLDivElement>(null);

  // Function to fetch account data
  const fetchAccountData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/alpaca/account', {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setAccountData(data);
    } catch (error) {
      console.error('Failed to fetch account data:', error);
      setError('Failed to load account data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Create ratio chart using Plot
  useEffect(() => {
    if (!accountData || !chartRef.current) return;

    const longValue = parseFloat(accountData.long_market_value);
    const shortValue = Math.abs(parseFloat(accountData.short_market_value));
    const total = longValue + shortValue;
    
    // Create data points for visualization
    const data = Array.from({ length: 50 }, (_, i) => ({
      x: i < (longValue / total) * 50 ? 'Long' : 'Short',
      y: Math.random(),
      value: i < (longValue / total) * 50 ? longValue : shortValue
    }));

    const plot = Plot.plot({
      height: 200,
      width: 400,
      padding: 20,
      grid: true,
      color: {
        domain: ['Long', 'Short'],
        range: ['#22c55e', '#ef4444']
      },
      marks: [
        Plot.dot(data, {
          x: "x",
          y: "y",
          fill: "x",
          title: d => `${d.x}: $${d.value.toLocaleString()}`
        })
      ]
    });

    chartRef.current.innerHTML = '';
    chartRef.current.append(plot);
    return () => plot.remove();
  }, [accountData]);

  // Initial data fetch
  useEffect(() => {
    fetchAccountData();
  }, []);

  // If there's an error, show it at the top
  if (error) {
    return (
      <div className="space-y-8">
        <Alert variant="error">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
        <Button 
          onClick={fetchAccountData} 
          variant="outline"
          size="sm"
        >
          <RefreshCw className="h-4 w-4 mr-2" />
          Try Again
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header with refresh button */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-white">Today</h2>
        <Button 
          onClick={fetchAccountData} 
          disabled={loading}
          variant="outline"
          size="sm"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {/* Main metrics grid */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Total Equity */}
        <Card className="col-span-2">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Equity</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-16 w-48 mx-auto" />
            ) : (
              <div className="text-4xl font-bold text-center py-4">
                ${accountData ? parseFloat(accountData.equity).toLocaleString() : '0'}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Cash */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Cash</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-8 w-32" />
            ) : (
              <div className="text-2xl font-bold">
                ${accountData ? parseFloat(accountData.cash).toLocaleString() : '0'}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Buying Power */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Buying Power</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-8 w-32" />
            ) : (
              <div className="text-2xl font-bold">
                ${accountData ? parseFloat(accountData.buying_power).toLocaleString() : '0'}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Long/Short Ratio Chart */}
        <Card className="col-span-2">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Long/Short Ratio</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-[200px] w-full" />
            ) : (
              <div ref={chartRef} className="flex justify-center" />
            )}
          </CardContent>
        </Card>

        {/* Daytrade Counter */}
        <Card className="col-span-2">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Daytrade Status</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-between">
                <Skeleton className="h-8 w-32" />
                <Skeleton className="h-8 w-32" />
              </div>
            ) : (
              <div className="flex items-center justify-between">
                <span className="text-xl">
                  {accountData ? `${accountData.daytrade_count}/4 daytrades used` : '0/4 daytrades used'}
                </span>
                {accountData?.pattern_day_trader && (
                  <span className="text-red-500 font-medium">Pattern Day Trader</span>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Note about auto-refresh */}
      <p className="text-sm text-muted-foreground">
        Note: Auto-refresh functionality coming soon. Currently using manual refresh.
      </p>
    </div>
  );
} 