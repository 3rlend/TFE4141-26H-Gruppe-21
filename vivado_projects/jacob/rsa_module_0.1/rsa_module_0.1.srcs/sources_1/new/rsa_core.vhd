----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/04/2026 05:44:25 PM
-- Design Name: 
-- Module Name: rsa_core - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity rsa_core is
    Port ( clk : in STD_LOGIC;
           msgin_valid : in STD_LOGIC;
           msgin_ready : out STD_LOGIC;
           msgin_last : in STD_LOGIC;
           msgin_data : in STD_LOGIC_VECTOR (255 downto 0);
           key_n : in STD_LOGIC_VECTOR (255 downto 0);
           key_e : in STD_LOGIC_VECTOR (255 downto 0);
           rsa_status : out STD_LOGIC_VECTOR (31 downto 0);
           msgout_valid : out STD_LOGIC;
           msgout_ready : in STD_LOGIC;
           msgout_last : out STD_LOGIC;
           msgout_data : out STD_LOGIC_VECTOR (255 downto 0));
end rsa_core;

architecture Behavioral of rsa_core is

begin

end Behavioral;
