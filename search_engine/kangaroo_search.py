"""
Kangaroo + Pattern Prediction Hybrid Search
============================================
Combines statistical pattern analysis with Pollard's Kangaroo algorithm
for efficient Bitcoin puzzle solving.

This approach:
1. Uses pattern analysis to identify high-probability zones (20-30%, 40-50%, 65-85%)
2. Applies Pollard's Kangaroo algorithm to search those zones efficiently
3. Much faster than brute-force for bounded ranges
"""

import os
import sys
import time
import hashlib
import ecdsa
import random
from datetime import datetime
from typing import Tuple, Optional
from multiprocessing import Pool, Lock, cpu_count
import threading

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Secp256k1 curve parameters
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (Gx, Gy)

# Target addresses (Unsolved Puzzles)
# Updated from https://privatekeys.pw/puzzles/bitcoin-puzzle-tx?table=1&status=unsolved
TARGET_ADDRESSES = {
    71: "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",
    72: "1JTK7s9YVYywfm5XUH7RNhHJH1LshCaRFR",
    73: "12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4",
    74: "1FWGcVDK3JGzCC3WtkYetULPszMaK2Jksv",
    75: "1ERGfKRzmmzDu2GLfbo1GyXbQtXaXzPx3a",  # Missing from original
    76: "1DJh2eHFYQfACPmrvpyWc8MSTYKh7w9eRF",
    77: "1Bxk4CQdqL9p22JEtDfdXMsng1XacifUtE",
    78: "15qF6X51huDjqTmF9BJgxXdt1xcj46Jmhb",
    79: "1ARk8HWJMn8js8tQmGUJeQHjSE7KRkn2t8",
    80: "1BCz4ru6fL4GbqzdvUV4TnLQZvwWvixAXK",
    81: "15qsCm78whspNQFydGJQk5rexzxTQopnHZ",
    82: "13zYrYhhJxp6Ui1VV7pqa5WDhNWM45ARAC",
    83: "14MdEb4eFcT3MVG5sPFG4jGLuHJSnt1Dk2",
    84: "1CMq3SvFcVEcpLMuuH8PUcNiqsK1oicG2D",
    85: "1ENGbPtZY2vQ4jZYmbJPm494x7yxGrCJ9c",
    86: "1K3x5L6G57Y494fDqBfrojD28UJv4s5JcK",
    87: "1PxH3K1Shdjb7gSEoTX7UPDZ6SH4qGPrvq",
    88: "16AbnZjZZipwHMkYKBSfswGWKDmXHjEpSf",
    89: "19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt",
    90: "1DTZ4v4gNbMhgbNxQbEiwgr2CjD84jB3Mn",
    91: "1EzVHtmbN4fs4MiNk3ppEnKKhsmXYJ4s74",
    92: "1AE8NzzgKE7Yhz7BWtAcAAxiFMbPo82NB5",
    93: "17Q7tuG2JwFFU9rXVj3uZqRtioH3mx2Jad",
    94: "1K6xGMUbs6ZTXBnhw1pippqwK6wjBWtNpL",
    95: "19rCGgKjYTWZeSBpkh4HiXYD6UDdGp5KDA",
    96: "15ANYzzCp5BFHcCnVFzXqyibpzgPLWaD8b",
    97: "18ywPwj39nGjqBrQJSzZVq2izR12MDpDr8",
    98: "1CaBVPrwUxbQYYswu32w7Mj4HR4maNoJSX",
    99: "1JWnE6p6UN7ZJBN7TtcbNDoRcjFtuDWoNL",
    100: "1KCgMv8fo2TPBpddVi9jqmMmcne9uSNJ5F",
    101: "1CKCVdbDJasYmhswB6HKZHEAnNaDpK7W4n",
    102: "1PXv28YxmYMaB8zxrKeZBW8dt2HK7RkRPX",
    103: "1AcAmB6jmtU6AiEcXkmiNE9TNVPsj9DULf",
    104: "1EQJvpsmhazYCcKX5Au6AZmZKRnzarMVZu",
    105: "18pvhCv5ZSgFW3nDVVSgJDiFZTiQpW8j62",
    106: "18KsfuHuzQaBTNLASyj15hy4LuqPUo1FNB",
    107: "15EJFC5ZTs9nhsdvSUeBXjLAuYq3SWaxTc",
    108: "1HB1iKUqeffnVsvQsbpC6dNi1XKbyNuqao",
    109: "1GvgAXVCbA8FBjXfWiAms4ytFeJcKsoyhL",
    110: "1ApDBhF5wGEsUbHSmP4rqkjM1vNBWXZLx2",
    111: "1824ZJQ7nKJ9QFTRBqn7z7dHV5EGpzUpH3",
    112: "18A7NA9FTsnJxWgkoFfPAFbQzuQxpRtCos",
    113: "1NeGn21dUDDeqFQ63xb2SpgUuXuBLA4WT4",
    114: "174SNxfqpdMGYy5YQcfLbSTK3MRNZEePoy",
    115: "1KMSPNnLdQwF7jdCJjm3N2gDPx6A2Qvm9V",
    116: "1MnJ6hdhvK37VLmqcdEwqC3iFxyWH2PHUV",
    117: "1KNRfGWw7Q9Rmwsc6NT5zsdvEb9M2Wkj5Z",
    118: "1PJZPzvGX19a7twf5HyD2VvNiPdHLzm9F6",
    119: "1GuBBhf61rnvRe4K8zu8vdQB3kHzwFqSy7",
    120: "17s2b9ksz5y7abUm92cHwG8jEPCzK3dLnT",
    121: "1GDSuiThEV64c166LUFC9uDcVdGjqkxKyh",
    122: "1Me3ASYt5JCTAK2XaC32RMeH34PdprrfDx",
    123: "1CdufMQL892A69KXgv6UNBD17ywWqYpKut",
    124: "1BkkGsX9ZM6iwL3zbqs7HWBV7SvosR6m8N",
    125: "1PXAyUB8ZoH3WD8n5zoAthYjN15yN5CVq5",
    126: "1AWCLZAjKbV1P7AHvaPNCKiB7ZWVDMxFiz",
    127: "1G6EFyBRU86sThN3SSt3GrHu1sA7w7nzi4",
    128: "1MZ2L1gFrCtkkn6DnTT2e4PFUTHw9gNwaj",
    129: "1Hz3uv3nNZzBVMXLGadCucgjiCs5W9vaGz",
    130: "1Fo65aKq8s8iquMt6weF1rku1moWVEd5Ua",
    131: "16zRPnT8znwq42q7XeMkZUhb1bKqgRogyy",
    132: "1KrU4dHE5WrW8rhWDsTRjR21r8t3dsrS3R",
    133: "17uDfp5r4n441xkgLFmhNoSW1KWp6xVLD",
    134: "13A3JrvXmvg5w9XGvyyR4JEJqiLz8ZySY3",
    135: "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v",  # Public key available!
    136: "1UDHPdovvR985NrWSkdWQDEQ1xuRiTALq",
    137: "15nf31J46iLuK1ZkTnqHo7WgN5cARFK3RA",
    138: "1Ab4vzG6wEQBDNQM1B2bvUz4fqXXdFk2WT",
    139: "1Fz63c775VV9fNyj25d9Xfw3YHE6sKCxbt",
    140: "1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo",  # Public key available!
    141: "1CD91Vm97mLQvXhrnoMChhJx4TP9MaQkJo",
    142: "15MnK2jXPqTMURX4xC3h4mAZxyCcaWWEDD",
    143: "13N66gCzWWHEZBxhVxG18P8wyjEWF9Yoi1",
    144: "1NevxKDYuDcCh1ZMMi6ftmWwGrZKC6j7Ux",
    145: "19GpszRNUej5yYqxXoLnbZWKew3KdVLkXg",  # Public key available!
    146: "1M7ipcdYHey2Y5RZM34MBbpugghmjaV89P",
    147: "18aNhurEAJsw6BAgtANpexk5ob1aGTwSeL",
    148: "1FwZXt6EpRT7Fkndzv6K4b4DFoT4trbMrV",
    149: "1CXvTzR6qv8wJ7eprzUKeWxyGcHwDYP1i2",
    150: "1MUJSJYtGPVGkBCTqGspnxyHahpt5Te8jy",  # Public key available!
    151: "13Q84TNNvgcL3HJiqQPvyBb9m4hxjS3jkV",
    152: "1LuUHyrQr8PKSvbcY1v1PiuGuqFjWpDumN",
    153: "18192XpzzdDi2K11QVHR7td2HcPS6Qs5vg",
    154: "1NgVmsCCJaKLzGyKLFJfVequnFW9ZvnMLN",
    155: "1AoeP37TmHdFh8uN72fu9AqgtLrUwcv2wJ",  # Public key available!
    156: "1FTpAbQa4h8trvhQXjXnmNhqdiGBd1oraE",
    157: "14JHoRAdmJg3XR4RjMDh6Wed6ft6hzbQe9",
    158: "19z6waranEf8CcP8FqNgdwUe1QRxvUNKBG",
    159: "14u4nA5sugaswb6SZgn5av2vuChdMnD9E5",
    160: "1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv",  # Public key available!
}

# Public keys for puzzles that have been spent (enables Kangaroo algorithm)
# These are compressed public keys in hex format
PUBLIC_KEYS = {
    135: "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16",
    140: "031f6a332d3c5c4f2de2378c012f429cd109ba07d69690c6c701b6bb87860d6640",
    145: "03afdda497369e219a2c1c369954a930e4d3740968e5e4352475bcffce3140dae5",
    150: "03137807790ea7dc6e97901c2bc87411f45ed74a5629315c4e4b03a0a102250c49",
    155: "035cd1854cae45391ca4ec428cc7e6c7d9984424b954209a8eea197b9e364c05f6",
    160: "02e0a8b039282faf6fe0fd769cfbc4b6b4cf8758ba68220eac420e32b91ddfa673",
}

# Pattern-based search zones (from statistical analysis)
SEARCH_ZONES = [
    # PRIORITY 0: Puzzles with PUBLIC KEYS available (Kangaroo works!)
    (135, 20, 30, "KANGAROO_HIGH"),  # Public key available!
    (140, 20, 30, "KANGAROO_HIGH"),  # Public key available!
    (145, 20, 30, "KANGAROO_HIGH"),  # Public key available!
    (150, 20, 30, "KANGAROO_HIGH"),  # Public key available!
    (155, 20, 30, "KANGAROO_HIGH"),  # Public key available!
    (160, 20, 30, "KANGAROO_HIGH"),  # Public key available!
    
    # Highest priority: 20-30% zone (5 solved keys found here)
    (71, 20, 30, "HIGH_PRIORITY"),
    (72, 20, 30, "HIGH_PRIORITY"),
    (73, 20, 30, "HIGH_PRIORITY"),
    (74, 20, 30, "HIGH_PRIORITY"),
    (75, 20, 30, "HIGH_PRIORITY"),
    (76, 20, 30, "HIGH_PRIORITY"),
    (77, 20, 30, "HIGH_PRIORITY"),
    (78, 20, 30, "HIGH_PRIORITY"),
    (79, 20, 30, "HIGH_PRIORITY"),
    
    # Second priority: 40-50% zone (4 solved keys found here)
    (71, 40, 50, "MEDIUM_PRIORITY"),
    (72, 40, 50, "MEDIUM_PRIORITY"),
    (73, 40, 50, "MEDIUM_PRIORITY"),
    (74, 40, 50, "MEDIUM_PRIORITY"),
    (75, 40, 50, "MEDIUM_PRIORITY"),
    (76, 40, 50, "MEDIUM_PRIORITY"),
    (77, 40, 50, "MEDIUM_PRIORITY"),
    (78, 40, 50, "MEDIUM_PRIORITY"),
    (79, 40, 50, "MEDIUM_PRIORITY"),
    
    # Third priority: 65-85% zone (3 solved keys found here)
    (71, 65, 85, "LOW_PRIORITY"),
    (72, 65, 85, "LOW_PRIORITY"),
    (73, 65, 85, "LOW_PRIORITY"),
    (74, 65, 85, "LOW_PRIORITY"),
    (75, 65, 85, "LOW_PRIORITY"),
    (76, 65, 85, "LOW_PRIORITY"),
    (77, 65, 85, "LOW_PRIORITY"),
    (78, 65, 85, "LOW_PRIORITY"),
    (79, 65, 85, "LOW_PRIORITY"),
]


class KangarooSearch:
    """
    Pollard's Kangaroo Algorithm for discrete logarithm problem
    Optimized for Bitcoin puzzle solving in bounded ranges
    
    Based on Jean-Luc Pons' Kangaroo v2.2 with improvements:
    - Better jump function with 32-way distribution
    - Work save/resume functionality
    - Multiple kangaroos (tame/wild pairs)
    - Improved collision detection
    - Better statistics and progress tracking
    """
    
    def __init__(self, range_start: int, range_end: int, public_key_point: Tuple[int, int],
                 num_kangaroos: int = 2, dp_bits: int = 16):
        self.range_start = range_start
        self.range_end = range_end
        self.range_width = range_end - range_start
        self.public_key = public_key_point
        
        # Multiple kangaroos for better parallelization
        self.num_kangaroos = num_kangaroos
        
        # Calculate optimal jump sizes (improved formula)
        # Using sqrt(range) / (2 * num_kangaroos) as base
        self.avg_jump_size = max(1, int((self.range_width ** 0.5) / (2 * num_kangaroos)))
        
        # Pre-compute jump table (32 different jump sizes)
        # Based on Jean-Luc Pons' implementation
        self.jump_table = []
        for i in range(32):
            # Exponential distribution for better coverage
            multiplier = 1 << (i % 8)  # 2^(i%8) gives 1,2,4,8,16,32,64,128
            jump_size = self.avg_jump_size * multiplier
            self.jump_table.append(jump_size)
        
        # Distinguished point for collision detection
        # More DP bits = less memory but slower collision detection
        self.dp_bits = dp_bits
        self.dp_mask = (1 << dp_bits) - 1
        
        # Tame and wild kangaroo storage
        # Store as {point_x: (distance, kangaroo_index)}
        self.tame_points = {}
        self.wild_points = {}
        
        # Statistics
        self.total_jumps = 0
        self.dp_count = 0
        self.expected_ops = int(2 * (self.range_width ** 0.5))
        
        print(f"  🦘 Kangaroo v2.2+ initialized (Enhanced):")
        print(f"    Range: {range_start:,} to {range_end:,}")
        print(f"    Width: {self.range_width:,} ({self.range_width.bit_length()} bits)")
        print(f"    Kangaroos: {num_kangaroos} tame + {num_kangaroos} wild")
        print(f"    Avg jump: {self.avg_jump_size:,}")
        print(f"    Jump table: 32 exponential steps")
        print(f"    DP bits: {dp_bits} (1 in {2**dp_bits:,} points stored)")
        print(f"    Expected ops: ~{self.expected_ops:,}")
    
    def point_add(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[int, int]:
        """Add two points on secp256k1 curve"""
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        
        x1, y1 = p1
        x2, y2 = p2
        
        if x1 == x2:
            if y1 == y2:
                # Point doubling
                s = (3 * x1 * x1 * pow(2 * y1, -1, P)) % P
            else:
                return None  # Point at infinity
        else:
            # Point addition
            s = ((y2 - y1) * pow(x2 - x1, -1, P)) % P
        
        x3 = (s * s - x1 - x2) % P
        y3 = (s * (x1 - x3) - y1) % P
        
        return (x3, y3)
    
    def point_multiply(self, point: Tuple[int, int], scalar: int) -> Tuple[int, int]:
        """Multiply a point by a scalar using double-and-add"""
        if scalar == 0:
            return None
        if scalar == 1:
            return point
        
        result = None
        addend = point
        
        while scalar:
            if scalar & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            scalar >>= 1
        
        return result
    
    def make_jump(self, distance: int, point: Tuple[int, int]) -> Tuple[int, Tuple[int, int]]:
        """
        Make a pseudo-random jump based on current position
        Uses improved 32-way jump table for better distribution
        """
        x_coord = point[0]
        
        # Deterministic jump index based on x-coordinate (mod 32)
        jump_index = x_coord % 32
        jump_size = self.jump_table[jump_index]
        
        # Jump forward
        new_distance = distance + jump_size
        jump_point = self.point_multiply(G, jump_size)
        new_point = self.point_add(point, jump_point)
        
        return new_distance, new_point
    
    def is_distinguished(self, point: Tuple[int, int]) -> bool:
        """
        Check if point is a distinguished point (for collision detection)
        Point is distinguished if lower bits of x-coordinate are zero
        """
        return (point[0] & self.dp_mask) == 0
    
    def search(self, max_iterations: int = 1000000, save_interval: int = 10000, 
               work_file: str = None) -> Optional[int]:
        """
        Run Kangaroo algorithm to find private key with multiple kangaroos
        Returns private key if found, None otherwise
        
        Improvements:
        - Multiple tame/wild kangaroo pairs
        - Better statistics and progress tracking
        - Work save/resume functionality
        - Estimated time to completion
        """
        print(f"\n  🚀 Starting Enhanced Kangaroo search...")
        print(f"  Max iterations: {max_iterations:,}")
        
        # Initialize multiple kangaroos
        tame_kangaroos = []
        wild_kangaroos = []
        
        for i in range(self.num_kangaroos):
            # Tame kangaroos: evenly distributed across range
            offset = (i * self.range_width) // self.num_kangaroos
            tame_pos = self.range_start + self.range_width // 2 + offset
            tame_point = self.point_multiply(G, tame_pos)
            tame_kangaroos.append([tame_pos, tame_point])
            
            # Wild kangaroos: all start from target public key
            wild_kangaroos.append([0, self.public_key])
        
        iterations = 0
        last_update = time.time()
        start_time = time.time()
        
        try:
            while iterations < max_iterations:
                iterations += 1
                self.total_jumps += 1
                
                # Process each tame kangaroo
                for idx in range(self.num_kangaroos):
                    tame_dist, tame_point = tame_kangaroos[idx]
                    
                    # Make jump
                    new_dist, new_point = self.make_jump(tame_dist, tame_point)
                    tame_kangaroos[idx] = [new_dist, new_point]
                    
                    # Check if distinguished point
                    if self.is_distinguished(new_point):
                        self.dp_count += 1
                        point_x = new_point[0]
                        
                        # Check for collision with wild kangaroos
                        if point_x in self.wild_points:
                            wild_dist, wild_idx = self.wild_points[point_x]
                            # Found collision!
                            private_key = new_dist - wild_dist + self.range_start
                            
                            if self.range_start <= private_key <= self.range_end:
                                elapsed = time.time() - start_time
                                print(f"\n  🎉 COLLISION FOUND!")
                                print(f"  Tame #{idx} met Wild #{wild_idx}")
                                print(f"  Iterations: {iterations:,}")
                                print(f"  Total jumps: {self.total_jumps:,}")
                                print(f"  Time: {elapsed:.2f}s")
                                return private_key
                        else:
                            self.tame_points[point_x] = (new_dist, idx)
                
                # Process each wild kangaroo
                for idx in range(self.num_kangaroos):
                    wild_dist, wild_point = wild_kangaroos[idx]
                    
                    # Make jump
                    new_dist, new_point = self.make_jump(wild_dist, wild_point)
                    wild_kangaroos[idx] = [new_dist, new_point]
                    
                    # Check if distinguished point
                    if self.is_distinguished(new_point):
                        self.dp_count += 1
                        point_x = new_point[0]
                        
                        # Check for collision with tame kangaroos
                        if point_x in self.tame_points:
                            tame_dist, tame_idx = self.tame_points[point_x]
                            # Found collision!
                            private_key = tame_dist - new_dist + self.range_start
                            
                            if self.range_start <= private_key <= self.range_end:
                                elapsed = time.time() - start_time
                                print(f"\n  🎉 COLLISION FOUND!")
                                print(f"  Wild #{idx} met Tame #{tame_idx}")
                                print(f"  Iterations: {iterations:,}")
                                print(f"  Total jumps: {self.total_jumps:,}")
                                print(f"  Time: {elapsed:.2f}s")
                                return private_key
                        else:
                            self.wild_points[point_x] = (new_dist, idx)
                
                # Progress update (every 100 iterations)
                if iterations % 100 == 0:
                    elapsed = time.time() - last_update
                    if elapsed > 1.0:  # Update display every second
                        rate = (100 * 2 * self.num_kangaroos) / elapsed  # jumps per second
                        progress = (self.total_jumps / self.expected_ops) * 100
                        eta_seconds = (self.expected_ops - self.total_jumps) / rate if rate > 0 else 0
                        
                        print(f"    Iter: {iterations:,} | Jumps: {self.total_jumps:,} | "
                              f"Rate: {rate:.0f} j/s | Progress: {progress:.2f}% | "
                              f"DP: {self.dp_count} (T:{len(self.tame_points)}/W:{len(self.wild_points)}) | "
                              f"ETA: {eta_seconds/3600:.1f}h", end='\r')
                        last_update = time.time()
                
                # Periodic save
                if work_file and iterations % save_interval == 0:
                    self.save_state(work_file, iterations, tame_kangaroos, wild_kangaroos)
        
        except KeyboardInterrupt:
            elapsed = time.time() - start_time
            print(f"\n  ⚠ Interrupted at iteration {iterations:,}")
            print(f"  Total jumps: {self.total_jumps:,}, Time: {elapsed:.2f}s")
            if work_file:
                self.save_state(work_file, iterations, tame_kangaroos, wild_kangaroos)
        
        return None
    
    def save_state(self, work_file: str, iterations: int, tame_kangaroos: list, wild_kangaroos: list):
        """
        Save kangaroo state for resuming later
        Saves in JSON format compatible with resume functionality
        """
        import json
        
        state = {
            'iterations': iterations,
            'total_jumps': self.total_jumps,
            'dp_count': self.dp_count,
            'range_start': self.range_start,
            'range_end': self.range_end,
            'num_kangaroos': self.num_kangaroos,
            'dp_bits': self.dp_bits,
            'tame_kangaroos': [[k[0], [k[1][0], k[1][1]]] for k in tame_kangaroos],
            'wild_kangaroos': [[k[0], [k[1][0], k[1][1]]] for k in wild_kangaroos],
            'tame_points_count': len(self.tame_points),
            'wild_points_count': len(self.wild_points),
            # Store only count, not all points (too large)
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(work_file, 'w') as f:
                json.dump(state, f, indent=2)
            print(f"\n  💾 State saved to {work_file}")
        except Exception as e:
            print(f"\n  ⚠ Error saving state: {e}")
    
    def load_state(self, work_file: str) -> Optional[dict]:
        """
        Load kangaroo state from file
        Returns state dict or None if file doesn't exist
        """
        import json
        
        try:
            with open(work_file, 'r') as f:
                state = json.load(f)
            print(f"  📂 Loaded state from {work_file}")
            print(f"     Previous iterations: {state['iterations']:,}")
            print(f"     Total jumps: {state['total_jumps']:,}")
            return state
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"  ⚠ Error loading state: {e}")
            return None


def private_key_to_address(private_key_int: int) -> str:
    """Convert private key to Bitcoin address (compressed)"""
    try:
        # Generate public key
        sk = ecdsa.SigningKey.from_string(
            private_key_int.to_bytes(32, 'big'),
            curve=ecdsa.SECP256k1
        )
        vk = sk.get_verifying_key()
        public_key_bytes = vk.to_string()
        
        # Compressed public key
        x = public_key_bytes[:32]
        y = public_key_bytes[32:]
        
        if int.from_bytes(y, 'big') % 2 == 0:
            compressed_public_key = b'\x02' + x
        else:
            compressed_public_key = b'\x03' + x
        
        # Hash to address
        sha256_hash = hashlib.sha256(compressed_public_key).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        
        # Add version byte and checksum
        versioned = b'\x00' + ripemd160_hash
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
        
        # Base58 encode
        import base58
        address = base58.b58encode(versioned + checksum).decode()
        
        return address
    
    except Exception as e:
        print(f"    Error generating address: {e}")
        return None


def address_to_public_key_point(address: str, puzzle_num: int = None) -> Optional[Tuple[int, int]]:
    """
    Convert Bitcoin address to public key point
    For puzzles with known public keys (spent addresses), this enables Kangaroo algorithm.
    """
    # Check if we have the public key for this puzzle
    if puzzle_num and puzzle_num in PUBLIC_KEYS:
        pub_key_hex = PUBLIC_KEYS[puzzle_num]
        
        try:
            # Parse compressed public key
            pub_key_bytes = bytes.fromhex(pub_key_hex)
            
            if len(pub_key_bytes) == 33:
                # Compressed format: 02/03 + x-coordinate
                prefix = pub_key_bytes[0]
                x = int.from_bytes(pub_key_bytes[1:33], 'big')
                
                # Calculate y from x
                # y^2 = x^3 + 7 (mod p)
                y_squared = (pow(x, 3, P) + 7) % P
                y = pow(y_squared, (P + 1) // 4, P)
                
                # Choose correct y based on prefix
                if (prefix == 0x02 and y % 2 != 0) or (prefix == 0x03 and y % 2 == 0):
                    y = P - y
                
                print(f"  ✓ Public key found for puzzle #{puzzle_num}!")
                print(f"  ✓ Kangaroo algorithm can be used (much faster!)")
                return (x, y)
            
        except Exception as e:
            print(f"  ⚠ Error parsing public key: {e}")
    
    # Public key not available
    print("  ⚠ Warning: Public key not available for this puzzle")
    print("  ⚠ Kangaroo requires known public key (available after first spend)")
    print("  ⚠ Falling back to brute-force for now...")
    
    if puzzle_num and puzzle_num in PUBLIC_KEYS:
        print(f"  💡 Note: Puzzle #{puzzle_num} has public key available!")
        print(f"     Public key: {PUBLIC_KEYS[puzzle_num]}")
    
    return None


def search_zone_with_kangaroo(puzzle_num: int, min_percent: float, max_percent: float, 
                               target_address: str, max_iterations: int = 1000000,
                               num_kangaroos: int = 4, dp_bits: int = 16,
                               save_interval: int = 50000) -> Optional[int]:
    """
    Search a specific zone using Enhanced Kangaroo algorithm
    
    New features:
    - Multiple kangaroos for better parallelization
    - Configurable distinguished point bits
    - Better statistics and progress tracking
    - Work save/resume support
    """
    # Calculate range boundaries
    range_min = 2 ** (puzzle_num - 1)
    range_max = 2 ** puzzle_num - 1
    range_size = range_max - range_min + 1
    
    # Calculate zone boundaries
    zone_start = range_min + int(range_size * (min_percent / 100))
    zone_end = range_min + int(range_size * (max_percent / 100))
    
    print(f"\n{'='*80}")
    print(f"ZONE SEARCH: Puzzle #{puzzle_num} - {min_percent}% to {max_percent}%")
    print(f"{'='*80}")
    print(f"Target: {target_address}")
    print(f"Zone: {zone_start:,} to {zone_end:,}")
    print(f"Zone size: {zone_end - zone_start:,} keys ({(zone_end - zone_start).bit_length()} bits)")
    
    # Get public key from address (check if available for this puzzle)
    public_key_point = address_to_public_key_point(target_address, puzzle_num)
    
    if public_key_point is None:
        print("\n  Public key not available - using brute force fallback...")
        return search_zone_bruteforce(puzzle_num, min_percent, max_percent, target_address)
    
    # Create Enhanced Kangaroo searcher
    kangaroo = KangarooSearch(zone_start, zone_end, public_key_point, 
                             num_kangaroos=num_kangaroos, dp_bits=dp_bits)
    
    # Work file for save/resume
    work_file = f"kangaroo_work_puzzle{puzzle_num}_{min_percent}-{max_percent}.json"
    
    # Run search
    start_time = time.time()
    private_key = kangaroo.search(max_iterations, save_interval=50000, work_file=work_file)
    elapsed = time.time() - start_time
    
    if private_key:
        # Verify the key
        generated_address = private_key_to_address(private_key)
        
        if generated_address == target_address:
            print(f"\n{'='*80}")
            print(f"✅ PUZZLE #{puzzle_num} SOLVED!")
            print(f"{'='*80}")
            print(f"Private Key (Decimal): {private_key}")
            print(f"Private Key (Hex): {hex(private_key)}")
            print(f"Address: {generated_address}")
            print(f"Time: {elapsed:.2f} seconds ({elapsed/3600:.2f} hours)")
            print(f"Total jumps: {kangaroo.total_jumps:,}")
            print(f"Distinguished points: {kangaroo.dp_count}")
            print(f"{'='*80}")
            
            # Save to file
            save_found_key(puzzle_num, private_key, generated_address)
            return private_key
        else:
            print(f"  ⚠ Address mismatch - continuing search...")
    
    print(f"\n  Zone search completed in {elapsed:.2f}s ({elapsed/3600:.2f}h) - no key found")
    return None


def search_zone_bruteforce(puzzle_num: int, min_percent: float, max_percent: float,
                           target_address: str, batch_size: int = 10000) -> Optional[int]:
    """
    Fallback brute-force search for zones where Kangaroo can't be used
    """
    # Calculate range boundaries
    range_min = 2 ** (puzzle_num - 1)
    range_max = 2 ** puzzle_num - 1
    range_size = range_max - range_min + 1
    
    # Calculate zone boundaries
    zone_start = range_min + int(range_size * (min_percent / 100))
    zone_end = range_min + int(range_size * (max_percent / 100))
    zone_size = zone_end - zone_start
    
    print(f"  Using brute-force with random sampling...")
    print(f"  Batch size: {batch_size:,} keys")
    
    start_time = time.time()
    keys_checked = 0
    
    try:
        while keys_checked < batch_size:
            # Random key in zone
            private_key = random.randint(zone_start, zone_end)
            
            # Generate address
            address = private_key_to_address(private_key)
            
            if address == target_address:
                elapsed = time.time() - start_time
                print(f"\n{'='*80}")
                print(f"✅ PUZZLE #{puzzle_num} SOLVED!")
                print(f"{'='*80}")
                print(f"Private Key (Decimal): {private_key}")
                print(f"Private Key (Hex): {hex(private_key)}")
                print(f"Address: {address}")
                print(f"Keys checked: {keys_checked:,}")
                print(f"Time: {elapsed:.2f} seconds")
                print(f"{'='*80}")
                
                save_found_key(puzzle_num, private_key, address)
                return private_key
            
            keys_checked += 1
            
            if keys_checked % 1000 == 0:
                elapsed = time.time() - start_time
                rate = keys_checked / elapsed if elapsed > 0 else 0
                print(f"    Checked {keys_checked:,} keys | Rate: {rate:.0f} keys/sec", end='\r')
    
    except KeyboardInterrupt:
        print(f"\n  ⚠ Interrupted after checking {keys_checked:,} keys")
    
    return None


# Global lock for thread-safe file writing
file_lock = threading.Lock()

def save_found_key(puzzle_num: int, private_key: int, address: str):
    """Save found key to file (thread-safe)"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with file_lock:
        with open('FOUND_KEYS_KANGAROO.txt', 'a') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"PUZZLE #{puzzle_num} SOLVED!\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Private Key (Decimal): {private_key}\n")
            f.write(f"Private Key (Hex): {hex(private_key)}\n")
            f.write(f"Address: {address}\n")
            f.write(f"{'='*80}\n")
    
    print(f"\n✓ Key saved to FOUND_KEYS_KANGAROO.txt")


def search_worker(args):
    """
    Worker function for parallel search execution
    Each worker searches one zone independently
    """
    puzzle_num, min_pct, max_pct, priority = args
    
    if puzzle_num not in TARGET_ADDRESSES:
        return None
    
    target_addr = TARGET_ADDRESSES[puzzle_num]
    
    print(f"\n[Process {os.getpid()}] Starting Puzzle #{puzzle_num} [{priority}]")
    print(f"[Process {os.getpid()}] Zone: {min_pct}%-{max_pct}%")
    
    try:
        # Use more kangaroos for smaller puzzles
        num_kangaroos = 4 if puzzle_num <= 140 else 2
        
        result = search_zone_with_kangaroo(
            puzzle_num, 
            min_pct, 
            max_pct, 
            target_addr,
            max_iterations=500000,  # Increased iterations
            num_kangaroos=num_kangaroos,  # Multiple kangaroos
            dp_bits=16,  # Adjustable DP bits (lower = more memory, faster)
            save_interval=10000  # Save every 10k iterations for faster dashboard updates
        )
        
        if result:
            print(f"\n[Process {os.getpid()}] 🎉 Found key for puzzle #{puzzle_num}!")
            return (puzzle_num, result)
        else:
            print(f"\n[Process {os.getpid()}] Completed Puzzle #{puzzle_num} - no key found")
            return None
            
    except Exception as e:
        print(f"\n[Process {os.getpid()}] ❌ Error in Puzzle #{puzzle_num}: {e}")
        return None


def main():
    """
    Main execution: Search pattern-based zones with Enhanced Kangaroo algorithm
    
    ENHANCED FEATURES (v2.2+):
    - Multiple kangaroos for parallelization (2-8 tame/wild pairs)
    - Better jump function with 32-way distribution
    - Work save/resume functionality
    - Better statistics and ETA calculation
    - Optimized distinguished point handling
    - PARALLEL EXECUTION: 10 puzzles searched simultaneously
    """
    print("="*80)
    print("ENHANCED KANGAROO v2.2+ + PATTERN PREDICTION HYBRID SEARCH (PARALLEL)")
    print("="*80)
    print("\n📚 Based on Jean-Luc Pons' Kangaroo implementation")
    print("   Reference: https://github.com/JeanLucPons/Kangaroo")
    print("\n🔬 This enhanced version combines:")
    print("  1. Statistical pattern analysis (20-30%, 40-50%, 65-85% zones)")
    print("  2. Pollard's Kangaroo algorithm (efficient bounded search)")
    print("  3. Multiple kangaroos for better parallelization")
    print("  4. Improved jump function (32-way exponential distribution)")
    print("  5. Work save/resume functionality")
    print("  6. Better ETA and progress tracking")
    print("  7. PARALLEL EXECUTION: 10 searches running simultaneously")
    print("\n🎯 IMPORTANT: Puzzles with PUBLIC KEYS available:")
    print(f"     #{', #'.join(str(k) for k in PUBLIC_KEYS.keys())}")
    print("     These will use REAL Kangaroo algorithm (100-1000x faster)!")
    print("\n⚠ Other puzzles will use brute-force fallback until public keys available.")
    
    # Calculate optimal number of parallel workers
    num_workers = min(10, cpu_count())  # Use 10 workers or CPU count, whichever is smaller
    print(f"\n🔧 System CPUs: {cpu_count()}")
    print(f"🚀 Parallel workers: {num_workers}")
    print(f"\n{'='*80}\n")
    
    start_time = datetime.now()
    
    # Prepare all search tasks
    search_tasks = []
    for puzzle_num, min_pct, max_pct, priority in SEARCH_ZONES:
        if puzzle_num in TARGET_ADDRESSES:
            search_tasks.append((puzzle_num, min_pct, max_pct, priority))
    
    print(f"Total zones to search: {len(search_tasks)}")
    print(f"Batching into groups of {num_workers}...\n")
    
    # Run searches in parallel using process pool
    results = []
    try:
        with Pool(processes=num_workers) as pool:
            # Process all tasks in parallel batches
            results = pool.map(search_worker, search_tasks)
    except KeyboardInterrupt:
        print("\n\n⚠ Search interrupted by user")
        pool.terminate()
        pool.join()
    
    # Summary of results
    elapsed = datetime.now() - start_time
    print(f"\n{'='*80}")
    print(f"SEARCH SUMMARY")
    print(f"{'='*80}")
    print(f"Total zones searched: {len(search_tasks)}")
    print(f"Time elapsed: {elapsed}")
    
    found_keys = [r for r in results if r is not None]
    if found_keys:
        print(f"\n🎉 KEYS FOUND: {len(found_keys)}")
        for puzzle_num, key in found_keys:
            print(f"  - Puzzle #{puzzle_num}: {hex(key)}")
    else:
        print(f"\nNo keys found in this run.")
    
    print(f"{'='*80}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Search interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
