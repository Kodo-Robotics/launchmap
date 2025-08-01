// Copyright (c) 2025 Kodo Robotics
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { defineConfig } from '@playwright/test';

export default defineConfig({
    testDir: './specs',
    snapshotDir: './__screenshots__',
    globalSetup: './fixtures/global-setup.js',
    use: {
        headless: true,
        viewport: { width: 1600, height: 900 },
        baseURL: process.env.TEST_SERVER_URL || 'http://localhost:3000',
    },
    reporter: [['list'], ['html']],
});